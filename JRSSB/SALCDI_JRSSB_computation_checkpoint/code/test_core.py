from pathlib import Path
import sys,json
import numpy as np
from paired_band import *
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'prior_core/jrssb_core_v1'))
from verify_core import covariance_example,critical_value

def run():
    rng=np.random.default_rng(8141);records=[]
    for j in [1,2,5]:
        a=rng.normal(size=(j,j));s=a@a.T+.6*np.eye(j)
        g=RadialGaussian(spherical_directions(j,16384,912));q,d=g.value_gradient(s)
        e=sym(rng.normal(size=(j,j)));ep=1e-6
        num=(g.value_gradient(s+ep*e,False)[0]-g.value_gradient(s-ep*e,False)[0])/(2*ep)
        ana=float(np.sum(d*e));err=abs(num-ana)/max(1,abs(ana))
        assert err<1e-5,(j,num,ana);records.append(dict(dimension=j,relative_error=err))
    om=covariance_example();g=RadialGaussian(spherical_directions(2,131072,291));integration=[]
    for w in [0,.1,25/41,1]:
        s=path_covariance(om,w);q=g.value_gradient(s,False)[0];exact=critical_value(s)
        assert abs(q-exact)<3e-5;integration.append(dict(weight=w,radial=q,exact=exact,error=q-exact))
    n,j=121,3;u=rng.normal(size=(n,j));b=rng.normal(size=(n,j));k=rng.uniform(.05,1,n)
    lm=local_moments(u,b,k,np.ones(n,bool),p_scale=.1,h_volume=.3)
    mat=sym(rng.normal(size=(2*j,2*j)));score=lm.covariance_scores(mat[None,:,:])[:,0]
    v=rng.normal(size=n);v-=v.mean();ep=1e-6
    def fn(e):
        w=(1+e*v)/n;mu=w@k;f=(w*k)@u/mu
        psi=np.sqrt(.1/.3)*k[:,None]*np.c_[u-f,b]
        return float(np.sum(mat*(psi.T@(w[:,None]*psi))))
    err=(fn(ep)-fn(-ep))/(2*ep)-np.mean(v*score);assert abs(err)<1e-7
    r=rng.uniform(size=n)<.2;pi=np.repeat(.2,n);q=np.tile([.2,.5,.8],(n,1));m=.8*q+.1;y=rng.normal(size=n);t=np.array([-1.,0.,1.])
    u1,b1=augmented_signals(y,r,pi,q,m,t);y[~r]=np.nan;u2,b2=augmented_signals(y,r,pi,q,m,t)
    assert np.array_equal(u1,u2) and np.array_equal(b1,b2)
    grid=np.array([0.,1.]);f=np.array([.1,.5]);x=np.array([-1,0,.2,1,1.9,2,3]);truth=np.array([0,.1,.1,.5,.5,1,1])
    lo,hi=monotone_envelope(grid,f-.05,f+.05,x);assert np.all((lo<=truth)&(truth<=hi))
    qa,qb=quantile_band(grid,f-.05,f+.05,[.05,.2,.8]);assert qa[2]==1 and np.isposinf(qb[2])
    u,b=augmented_signals(y,r,pi,q,q,t);lm=local_moments(u,b,k,r,p_scale=.2,h_volume=.4)
    sel=paired_calibration(lm,RadialGaussian(spherical_directions(3,1024,77)),np.linspace(0,1,11))
    assert sel['weight']==0 and sel['zero_path']
    return dict(passed=True,gradient_checks=records,radial_quadrature_checks=integration,centering_error=float(err),leakage_test=True,atomic_envelope=True,zero_path=True)
if __name__=='__main__':
    a=run();p=Path(__file__).resolve().parents[1]/'results/unit_tests.json';p.write_text(json.dumps(a,indent=2));print(json.dumps(a,indent=2))
