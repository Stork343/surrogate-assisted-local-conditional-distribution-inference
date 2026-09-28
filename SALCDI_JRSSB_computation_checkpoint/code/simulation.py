"""Paired simulations: fitted candidates, independent gate/evaluation, known truth.

Population quadrature is used only for assessment, never by a fitted procedure.
All failed calculations remain in the result table as explicitly flagged trivial
bands. A run manifest is written before computation. Seeds do not depend on worker
scheduling. Rerunning with the same configuration reproduces every table row.
"""
from __future__ import annotations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
import argparse,json,time,hashlib,traceback
from pathlib import Path
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
from scipy import special,stats
from numpy.polynomial.legendre import leggauss
from numpy.polynomial.hermite import hermgauss
from paired_band import *
ROOT=Path(__file__).resolve().parents[1]

def mu(x):return 1.2*x+.6*x*x

def sigma(x):return .8+.25*x*x

def loading(x,scenario):
    if scenario=='reversal':return np.where(abs(x)<=.4,-1.,1.)
    if scenario=='no_signal':return np.zeros_like(x)
    return np.ones_like(x)

def noise(scenario):return 1.6 if scenario=='weak' else .4

def probabilities(x,s,p,scenario,design):
    if design=='random':return np.full_like(x,p)
    t=loading(x,scenario);sd=np.sqrt(t*t*sigma(x)**2+noise(scenario)**2)
    return p*(1+.4*np.tanh((s-t*mu(x))/sd))

def generate(n,p,scenario,design,rng):
    x=rng.uniform(-1,1,n);y=mu(x)+sigma(x)*rng.normal(size=n)
    s=loading(x,scenario)*y+noise(scenario)*rng.normal(size=n)
    pi=probabilities(x,s,p,scenario,design);r=rng.uniform(size=n)<pi
    return x,y,s,r,pi

def regressors(x,s,surrogate):
    return np.c_[np.ones(len(x)),x,x*x,s] if surrogate else np.c_[np.ones(len(x)),x,x*x]

@dataclass
class Candidate:
    coefficient:np.ndarray
    sd:float
    surrogate:bool
    def predict(self,x,s,thresholds):
        mean=regressors(x,s,self.surrogate)@self.coefficient
        return special.ndtr((thresholds[None,:]-mean[:,None])/self.sd)

def fit_candidate(x,y,s,r,pi,surrogate):
    if np.sum(r)<10:raise InsufficientInformation('fewer than 10 training references')
    a=regressors(x[r],s[r],surrogate);w=np.ones(np.sum(r)) if surrogate else 1/pi[r]
    b=np.linalg.lstsq(a*np.sqrt(w)[:,None],y[r]*np.sqrt(w),rcond=None)[0]
    residual=y[r]-a@b;v=np.sum(w*residual**2)/np.sum(w)
    return Candidate(b,float(np.sqrt(max(v,1e-4))),surrogate)

def truth_and_covariance(qfit,mfit,p,scenario,design,h,thresholds,nx=48,ns=24):
    xx,wx=leggauss(nx);x=h*xx;wx=wx*h/2
    z,wz=hermgauss(ns);z=z*np.sqrt(2);wz=wz/np.sqrt(np.pi)
    xn=np.repeat(x,ns);w=np.repeat(wx,ns)*np.tile(wz,nx)
    t=loading(xn,scenario);ss=np.sqrt(t*t*sigma(xn)**2+noise(scenario)**2)
    sn=t*mu(xn)+ss*np.tile(z,nx);k=kernel(xn,0,h)
    pi=probabilities(xn,sn,p,scenario,design)
    cm=mu(xn)+t*sigma(xn)**2/ss**2*(sn-t*mu(xn))
    cs=sigma(xn)*noise(scenario)/ss
    m0=special.ndtr((thresholds[None,:]-cm[:,None])/cs[:,None])
    f=((wx*kernel(x,0,h))[:,None]*special.ndtr((thresholds[None,:]-mu(x)[:,None])/sigma(x)[:,None])).sum(0)/(wx@kernel(x,0,h))
    q=qfit.predict(xn,sn,thresholds);m=mfit.predict(xn,sn,thresholds)
    if scenario=='zero_path':m=q.copy()
    d=m-q;res=q-m0;between=m0-f;j=len(thresholds)
    c=m0[:,np.minimum.outer(np.arange(j),np.arange(j))]-m0[:,:,None]*m0[:,None,:]
    ww=w*k*k*p/h;wv=ww*(1/pi-1)
    a=np.einsum('n,nij->ij',ww/pi,c)+res.T@(wv[:,None]*res)+between.T@(ww[:,None]*between)
    cross=res.T@(wv[:,None]*d);v=d.T@(wv[:,None]*d)
    return f,sym(np.block([[a,cross],[cross.T,v]]))

def prepare(cell,rep,config):
    seed=int(config['seed']+cell['id']*100000+rep);rng=np.random.default_rng(seed)
    n,p=cell['n'],cell['p'];sc,design=cell['scenario'],cell['design'];h=config['bandwidth']
    thresholds=.8*stats.norm.ppf(np.linspace(.1,.9,config['thresholds']))
    x,y,s,r,pi=generate(n,p,sc,design,rng)
    n3=n//3;ti=np.arange(n3);gi=np.arange(n3,2*n3);ei=np.arange(2*n3,n)
    qf=fit_candidate(x[ti],y[ti],s[ti],r[ti],pi[ti],False)
    mf=fit_candidate(x[ti],y[ti],s[ti],r[ti],pi[ti],True)
    q=qf.predict(x,s,thresholds);m=mf.predict(x,s,thresholds)
    if sc=='zero_path':m=q.copy()
    yy=y.copy();yy[~r]=np.nan
    u,b=augmented_signals(yy,r,pi,q,m,thresholds);k=kernel(x,0,h)
    return dict(seed=seed,x=x,y=y,s=s,r=r,pi=pi,qf=qf,mf=mf,u=u,b=b,k=k,gi=gi,ei=ei,thresholds=thresholds)

def one_rep(task):
    cell,rep,config=task
    p=cell['p'];sc=cell['scenario'];h=config['bandwidth'];j=config['thresholds']
    z=prepare(cell,rep,config);u,b,k=z['u'],z['b'],z['k'];gi,ei=z['gi'],z['ei'];r=z['r']
    gate=local_moments(u[gi],b[gi],k[gi],r[gi],p_scale=p,h_volume=h)
    wg=np.linspace(0,1,config['weight_count'])
    integ=RadialGaussian(spherical_directions(j,config['directions'],7241),.05,config['ridge'])
    selection=paired_calibration(gate,integ,wg,delta=config['delta'],multiplier_draws=config['multipliers'],seed=z['seed']+71,remainder=config['remainder'])
    truth,omega=truth_and_covariance(z['qf'],z['mf'],p,sc,cell['design'],h,z['thresholds'])
    oracle_integ=RadialGaussian(spherical_directions(j,config['oracle_directions'],9091),.05,config['ridge'])
    oracle_c=np.array([oracle_integ.value_gradient(path_covariance(omega,w),False)[0] for w in wg])
    c0=oracle_c[0];oracle_min=float(oracle_c.min())
    methods={'Anchor':0.,'Full':1.,'Trace':selection['trace_weight'],
             'Plug-in band':selection['plugin_weight'],'Paired':selection['weight']}
    # A richer ridge-regularised control-variate projection, fixed ridge rule.
    vv=gate.omega[j:,j:];ridge=.05*max(float(np.trace(vv))/j,1e-12)
    projection=-gate.omega[:j,j:]@np.linalg.pinv(vv+ridge*np.eye(j),rcond=1e-12)
    methods['Projection']=None
    evaluation=RadialGaussian(spherical_directions(j,config['evaluation_directions'],14511),.05,config['ridge'])
    rows=[];outputs={}
    for name,weight in methods.items():
        warning=''
        if name=='Projection':
            uu=u[ei]+b[ei]@projection.T;bb=np.zeros_like(uu);ww=0.
            hh=np.c_[np.eye(j),projection];ct=oracle_integ.value_gradient(sym(hh@omega@hh.T),False)[0]
        else:
            uu=u[ei];bb=b[ei];ww=weight
            ct=oracle_integ.value_gradient(path_covariance(omega,weight),False)[0]
        try:
            fit=evaluate_band(uu,bb,k[ei],ww,p_scale=p,h_volume=h,integrator=evaluation)
            cover=bool(np.all((fit['lower']<=truth)&(truth<=fit['upper'])))
            half=fit['half_width'];est=fit['estimate']
        except InsufficientInformation as exc:
            warning=str(exc);mu_e=np.mean(k[ei]);est=np.mean(k[ei,None]*(uu+ww*bb),axis=0)/mu_e
            cover=True;half=.5 # explicit [0,1] fallback, not a centred normal band
        outputs[name]=(est,half)
        rows.append(dict(cell_id=cell['id'],scenario=sc,design=cell['design'],n=cell['n'],p=p,replicate=rep,seed=z['seed'],method=name,
                         weight=np.nan if weight is None else float(weight),coverage=cover,half_width=half,
                         ise=float(np.mean((est-truth)**2)),true_critical=float(ct),true_gain=float(c0-ct),
                         harm_numeric=bool(ct>c0+config['harm_tolerance']),
                         oracle_regret=float(ct-oracle_min) if name!='Projection' else np.nan,
                         certified_lower=float(selection['lower_gain'][selection['index']]) if name=='Paired' else np.nan,
                         gate_references=gate.verified_support,evaluation_references=int(np.sum(r[ei]&(k[ei]>0))),
                         gate_radius=selection['slope_radius'],fallback=bool(warning),warning=warning))
    anchor_half=outputs['Anchor'][1];anchor_ise=float(np.mean((outputs['Anchor'][0]-truth)**2))
    for row in rows:
        row['paired_width_ratio']=row['half_width']/anchor_half
        row['paired_ise_difference']=row['ise']-anchor_ise
    return rows

def safe_rep(task):
    try:return one_rep(task)
    except Exception as e:
        cell,rep,cfg=task
        return [dict(cell_id=cell['id'],scenario=cell['scenario'],design=cell['design'],n=cell['n'],p=cell['p'],replicate=rep,method='RUN_ERROR',warning=repr(e),traceback=traceback.format_exc())]

def default_cells():
    cells=[]
    for design in ['random','selective']:
        for p in [.05,.1,.2]:cells.append(dict(scenario='aligned',design=design,p=p,n=6000))
    for sc in ['weak','reversal','no_signal','zero_path']:cells.append(dict(scenario=sc,design='random',p=.1,n=6000))
    cells.append(dict(scenario='aligned',design='random',p=.1,n=12000))
    cells.append(dict(scenario='reversal',design='selective',p=.1,n=6000))
    for i,c in enumerate(cells):c['id']=i+1
    return cells

def summarise(df):
    good=df[df.method!='RUN_ERROR'].copy();group=['cell_id','scenario','design','n','p','method'];rows=[]
    for key,d in good.groupby(group,sort=True):
        row=dict(zip(group,key));row['replications']=len(d)
        for col in ['coverage','half_width','ise','weight','true_gain','harm_numeric','oracle_regret','paired_width_ratio','paired_ise_difference','gate_references','evaluation_references','fallback']:
            v=pd.to_numeric(d[col],errors='coerce').dropna().to_numpy(float)
            row[col]=float(v.mean()) if len(v) else np.nan
            row[col+'_mcse']=float(v.std(ddof=1)/np.sqrt(len(v))) if len(v)>1 else np.nan
        row['positive_borrowing']=float((d.weight.fillna(0)>0).mean())
        rows.append(row)
    return pd.DataFrame(rows)

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--reps',type=int,default=500);pa.add_argument('--workers',type=int,default=4)
    pa.add_argument('--output',default='main');pa.add_argument('--cells',default='all');pa.add_argument('--directions',type=int,default=2048)
    pa.add_argument('--thresholds',type=int,default=7);pa.add_argument('--no-remainder',action='store_true')
    args=pa.parse_args();out=ROOT/'results'/args.output;out.mkdir(parents=True,exist_ok=True)
    cfg=dict(seed=2026092801,bandwidth=.35,thresholds=args.thresholds,weight_count=11,delta=.05,multipliers=1999,
             directions=args.directions,oracle_directions=8192,evaluation_directions=8192,ridge=0.,remainder=not args.no_remainder,
             harm_tolerance=1e-4,replications=args.reps,workers=args.workers)
    cells=default_cells()
    if args.cells!='all':
        requested={int(x) for x in args.cells.split(',')};cells=[c for c in cells if c['id'] in requested]
    manifest=dict(config=cfg,cells=cells,created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                  code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    tasks=[(c,i,cfg) for c in cells for i in range(args.reps)]
    t=time.time();all_rows=[]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for k,rows in enumerate(pool.map(safe_rep,tasks,chunksize=4),1):
            all_rows.extend(rows)
            if k%25==0 or k==len(tasks):print(f'{k}/{len(tasks)} replications; {time.time()-t:.1f}s',flush=True)
    df=pd.DataFrame(all_rows);df.to_csv(out/'replicates.csv',index=False)
    summarise(df).to_csv(out/'summary.csv',index=False)
    errors=df[df.method=='RUN_ERROR']
    (out/'completion.json').write_text(json.dumps(dict(completed_replications=len(tasks),run_errors=len(errors),rows=len(df),elapsed_seconds=time.time()-t),indent=2))
    print('Done',out,'errors=',len(errors),flush=True)
    if len(errors):raise SystemExit(2)

if __name__=='__main__':main()
