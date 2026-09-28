"""Dependence-valid three-role rotation: union-bound, not a pooled bootstrap.

Each role fit is honest relative to its own evaluation fold. Across rotations
no independence is assumed. Both convex aggregation and intersection of the
Bonferroni-calibrated bands are evaluated. The point estimate is the equal
average of the three role-specific estimates.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import json,time
import numpy as np,pandas as pd
from scipy import stats
from simulation import generate,fit_candidate,truth_and_covariance
from paired_band import *
ROOT=Path(__file__).resolve().parents[1]

def worker(arg):
    scenario,rep=arg
    seed=2026092829+(0 if scenario=='aligned' else 100000)+rep
    rg=np.random.default_rng(seed);n=6000;p=.1;h=.35;j=7
    x,y,s,r,pi=generate(n,p,scenario,'random',rg)
    th=.8*stats.norm.ppf(np.linspace(.1,.9,j));k=kernel(x,0,h)
    folds=np.array_split(np.arange(n),3);outputs={'Anchor':[],'Paired':[]};weights=[]
    g=RadialGaussian(spherical_directions(j,4096,7441),alpha=.05/3)
    e=RadialGaussian(spherical_directions(j,8192,8431),alpha=.05/3)
    for z in range(3):
        ti,gi,ei=folds[z],folds[(z+1)%3],folds[(z+2)%3]
        qf=fit_candidate(x[ti],y[ti],s[ti],r[ti],pi[ti],False)
        mf=fit_candidate(x[ti],y[ti],s[ti],r[ti],pi[ti],True)
        q=qf.predict(x,s,th);m=mf.predict(x,s,th)
        yy=y.copy();yy[~r]=np.nan
        u,b=augmented_signals(yy,r,pi,q,m,th)
        mom=local_moments(u[gi],b[gi],k[gi],r[gi],p_scale=p,h_volume=h)
        sel=paired_calibration(mom,g,np.linspace(0,1,11),delta=.05/3,seed=seed+z+13)
        weights.append(sel['weight'])
        for name,w in [('Anchor',0.),('Paired',sel['weight'])]:
            fit=evaluate_band(u[ei],b[ei],k[ei],w,p_scale=p,h_volume=h,integrator=e)
            outputs[name].append(fit)
        truth,_=truth_and_covariance(qf,mf,p,scenario,'random',h,th)
    out=[]
    for name,ff in outputs.items():
        point=np.mean([z['estimate'] for z in ff],axis=0)
        meanlo=np.mean([z['lower'] for z in ff],axis=0);meanhi=np.mean([z['upper'] for z in ff],axis=0)
        maxlo=np.max([z['lower'] for z in ff],axis=0);minhi=np.min([z['upper'] for z in ff],axis=0)
        empty=bool(np.any(maxlo>minhi))
        if empty:maxlo=np.zeros(j);minhi=np.ones(j)
        out.append(dict(scenario=scenario,replicate=rep,method=name,seed=seed,
                        convex_coverage=bool(np.all((meanlo<=truth)&(truth<=meanhi))),
                        convex_mean_width=float(np.mean(meanhi-meanlo)),
                        intersection_coverage=bool(np.all((maxlo<=truth)&(truth<=minhi))),
                        intersection_mean_width=float(np.mean(minhi-maxlo)),empty_intersection=empty,
                        ise=float(np.mean((point-truth)**2)),mean_weight=np.mean(weights) if name=='Paired' else 0.))
    return out

def run():
    args=[(s,r) for s in ['aligned','reversal'] for r in range(200)]
    rows=[];t=time.time()
    with ProcessPoolExecutor(max_workers=4) as pool:
        for j,z in enumerate(pool.map(worker,args),1):
            rows.extend(z)
            if j%25==0:print(j,'/',len(args),round(time.time()-t,1),flush=True)
    d=pd.DataFrame(rows);d.to_csv(ROOT/'results/rotation_replicates.csv',index=False)
    out=d.groupby(['scenario','method']).agg(replications=('replicate','size'),convex_coverage=('convex_coverage','mean'),
        convex_mean_width=('convex_mean_width','mean'),intersection_coverage=('intersection_coverage','mean'),
        intersection_mean_width=('intersection_mean_width','mean'),empty_intersections=('empty_intersection','sum'),
        ise=('ise','mean'),mean_weight=('mean_weight','mean')).reset_index()
    out.to_csv(ROOT/'results/rotation_summary.csv',index=False)
    print(out.to_string(index=False),flush=True)
if __name__=='__main__':run()
