"""Local simultaneous inference with paired-gain multiplier calibration.

The implemented selector has an asymptotic guarantee. It is not the exact
finite-sample covariance-set selector. Numerical integration uses a fixed,
reproducible spherical quadrature; its accuracy is audited separately. No missing
reference outcome is used. No covariance eigenvalue is silently repaired.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np
from scipy import linalg,special,stats,optimize

class InsufficientInformation(ValueError):
    pass

def sym(a):return (a+a.T)*.5

def kernel(x,x0,h):
    if h<=0:raise ValueError('bandwidth must be positive')
    u=(np.asarray(x,float)-x0)/h
    return .75*np.maximum(0.,1-u*u)

def spherical_directions(j,draws,seed,quasi=True):
    if j<1 or draws<16:raise ValueError('invalid integration size')
    if quasi:
        u=stats.qmc.Sobol(j,scramble=True,seed=seed).random_base2(int(np.ceil(np.log2(draws))))[:draws]
        z=special.ndtri(np.clip(u,1e-15,1-1e-15))
    else:z=np.random.default_rng(seed).normal(size=(draws,j))
    return z/np.linalg.norm(z,axis=1)[:,None]

@dataclass
class RadialGaussian:
    directions:np.ndarray
    alpha:float=.05
    ridge:float=0.
    def __post_init__(self):
        self.directions=np.asarray(self.directions,float)
        if not 0<self.alpha<1 or self.ridge<0:raise ValueError('invalid calibration')
        if not np.allclose((self.directions**2).sum(1),1,atol=1e-8):raise ValueError('nonunit directions')
    def value_gradient(self,covariance,gradient=True,probability=None):
        s=sym(np.asarray(covariance,float));j=len(s)
        if s.shape!=(j,j) or self.directions.shape[1]!=j:raise ValueError('dimension mismatch')
        s=s+self.ridge*np.eye(j);prob=1-self.alpha if probability is None else probability
        if not 0<prob<1:raise ValueError('probability outside (0,1)')
        if j==1:
            if s[0,0]<=0:raise InsufficientInformation('nonpositive variance')
            z=stats.norm.ppf((1+prob)/2)
            return float(z*np.sqrt(s[0,0])),np.array([[z/(2*np.sqrt(s[0,0]))]]) if gradient else None
        try:l=np.linalg.cholesky(s)
        except np.linalg.LinAlgError as e:raise InsufficientInformation('output covariance not positive definite') from e
        u=self.directions;v=u@l.T;idx=np.argmax(abs(v),axis=1);vm=v[np.arange(len(u)),idx];m=abs(vm)
        def cdf(t):return float(np.mean(special.gammainc(j/2,.5*(t/m)**2)))
        upper=np.sqrt(np.diag(s).max())*stats.norm.ppf(1-(1-prob)/(2*j))
        while cdf(upper)<prob:upper*=1.25
        q=float(optimize.brentq(lambda t:cdf(t)-prob,0.,upper,xtol=1e-11,rtol=1e-12))
        if not gradient:return q,None
        a=q/m
        den=np.exp((1-j/2)*np.log(2)-special.gammaln(j/2)+(j-1)*np.log(a)-.5*a*a)
        ht=float(np.mean(den/m))
        if ht<=0:raise InsufficientInformation('zero calibration density')
        dl=np.zeros((j,j));weight=-den*q/(m*m)*np.sign(vm)
        np.add.at(dl,idx,weight[:,None]*u/len(u))
        aa=l.T@dl;middle=.5*(np.tril(aa)+np.tril(aa,-1).T)
        il=linalg.solve_triangular(l,np.eye(j),lower=True)
        return q,sym(-(il.T@middle@il)/ht)
    def iid_dkw_interval(self,covariance,failure,comparisons=1):
        """ONLY iid directions, fixed finite comparison family independent of them."""
        eps=np.sqrt(np.log(2*comparisons/failure)/(2*len(self.directions)))
        a,b=1-self.alpha-eps,1-self.alpha+eps
        return (0. if a<=0 else self.value_gradient(covariance,False,a)[0],
                float('inf') if b>=1 else self.value_gradient(covariance,False,b)[0])

def augmented_signals(y,r,pi,q,m,thresholds,contrast=None):
    y=np.asarray(y,float);r=np.asarray(r,bool);pi=np.asarray(pi,float)
    q=np.asarray(q,float);m=np.asarray(m,float);t=np.asarray(thresholds,float)
    n=len(y)
    if r.shape!=(n,) or pi.shape!=(n,) or q.shape!=(n,len(t)) or m.shape!=q.shape:raise ValueError('dimensions disagree')
    if np.any(~np.isfinite(y[r])) or np.any(~np.isfinite(pi)) or np.any((pi<=0)|(pi>1)):raise ValueError('invalid observed data')
    if np.any(~np.isfinite(q)) or np.any(~np.isfinite(m)) or np.any((q<0)|(q>1)|(m<0)|(m>1)):raise ValueError('invalid candidate CDF')
    u=q.copy();u[r]+=((y[r,None]<=t).astype(float)-q[r])/pi[r,None]
    b=(1-r.astype(float)/pi)[:,None]*(m-q)
    if contrast is not None:
        c=np.asarray(contrast,float)
        if c.shape!=u.shape or not np.isfinite(c).all():raise ValueError('invalid contrast')
        u-=c
    return u,b

@dataclass
class LocalMoments:
    estimate:np.ndarray
    omega:np.ndarray
    psi:np.ndarray
    mean_derivative:np.ndarray
    estimate_influence:np.ndarray
    kernel_mean:float
    n:int
    verified_support:int
    h_volume:float
    p_scale:float
    def covariance_scores(self,gradients):
        g=np.asarray(gradients,float);j=len(self.estimate)
        a=np.einsum('ni,lij,nj->nl',self.psi,g,self.psi,optimize=True)
        a-=np.einsum('lij,ij->l',g,self.omega)[None,:]
        ga=np.einsum('lij,j->li',g,self.mean_derivative)[:,:j]
        a-=2*self.estimate_influence@ga.T
        return a-a.mean(0,keepdims=True)

def local_moments(u,b,k,r,*,p_scale,h_volume):
    u=np.asarray(u,float);b=np.asarray(b,float);k=np.asarray(k,float);n,j=u.shape
    if b.shape!=u.shape or k.shape!=(n,) or np.any(k<0):raise ValueError('invalid moments')
    mu=float(k.mean())
    if n<3 or mu<=0 or p_scale<=0 or h_volume<=0:raise InsufficientInformation('empty local sample')
    f=(k[:,None]*u).mean(0)/mu
    res=np.c_[u-f,b];psi=np.sqrt(p_scale/h_volume)*k[:,None]*res
    om=sym(psi.T@psi/n)
    a=(p_scale/h_volume)*(k[:,None]**2*res).mean(0)
    ell=k[:,None]*(u-f)/mu
    return LocalMoments(f,om,psi,a,ell,mu,n,int(np.sum((k>0)&np.asarray(r,bool))),h_volume,p_scale)

def path_covariance(om,w):
    j=len(om)//2
    return sym(om[:j,:j]+w*(om[:j,j:]+om[j:,:j])+w*w*om[j:,j:])

def lifted_gradient(g,w):return np.block([[g,w*g],[w*g,w*w*g]])

def upper_empirical_quantile(values,probability,error=None):
    a=np.asarray(values,float)
    if error is None:return float(np.quantile(a,probability,method='higher'))
    rank=int(stats.binom.ppf(1-error,len(a),probability))+1
    return float('inf') if rank>len(a) else float(np.partition(a,rank-1)[rank-1])

def paired_calibration(moments,integrator,weights,*,delta=.05,multiplier_draws=1999,seed=1,remainder=True,numerical_error=None):
    weights=np.asarray(weights,float)
    if weights[0]!=0 or np.any(np.diff(weights)<=0) or weights[-1]>1 or not 0<delta<.5:raise ValueError('invalid weights/confidence')
    om=moments.omega;j=len(moments.estimate);c=[];grad=[]
    for w in weights:
        q,d=integrator.value_gradient(path_covariance(om,float(w)))
        c.append(q);grad.append(lifted_gradient(d,w))
    c=np.asarray(c);grad=np.asarray(grad);gains=c[0]-c;gains[0]=0.
    vv=float(np.trace(om[j:,j:]));cv=float(np.trace(om[:j,j:]))
    trace=float(np.clip(-cv/vv,0,1)) if vv>0 else 0.
    if abs(om[j:,j:]).max()<1e-25:
        return dict(weight=0.,index=0,critical_values=c,gains=gains,lower_gain=np.zeros_like(c),slope_radius=0.,remainder=0.,weights=weights,trace_weight=0.,plugin_weight=0.,zero_path=True,numerical_gain_protection=False)
    dg=(grad[0][None,:,:]-grad[1:])/weights[1:,None,None]
    scores=moments.covariance_scores(dg)
    cov=sym(scores.T@scores/moments.n**2)
    ev,v=np.linalg.eigh(cov);root=v*np.sqrt(np.maximum(ev,0))
    draw=np.random.default_rng(seed).normal(size=(multiplier_draws,len(weights)-1))@root.T
    radius=upper_empirical_quantile(np.maximum(0.,draw.max(1)),1-delta)
    count=max(moments.verified_support,1)
    cushion=c[0]*np.log1p(count)/count if remainder else 0.
    penalty=weights*(radius+cushion)
    if numerical_error is not None:
        en=np.asarray(numerical_error,float)
        if en.shape!=weights.shape or en[0]!=0 or np.any(en<0):raise ValueError('invalid integration error bounds')
        penalty+=en
    lower=gains-penalty;lower[0]=0.
    chosen=int(np.argmax(lower))
    if lower[chosen]<=0:chosen=0
    return dict(weight=float(weights[chosen]),index=chosen,critical_values=c,gains=gains,lower_gain=lower,
                slope_radius=float(radius+cushion),bootstrap_radius=float(radius),remainder=float(cushion),
                weights=weights,trace_weight=trace,plugin_weight=float(weights[np.argmin(c)]),zero_path=False,
                score_covariance=cov,numerical_gain_protection=numerical_error is not None)

def evaluate_band(u0,b,k,weight,*,p_scale,h_volume,integrator):
    n=len(k);mu=float(np.mean(k))
    if mu<=0:raise InsufficientInformation('empty evaluation support')
    u=u0+weight*b;f=(k[:,None]*u).mean(0)/mu
    psi=np.sqrt(p_scale/h_volume)*k[:,None]*(u-f)
    cov=sym(psi.T@psi/n);crit=integrator.value_gradient(cov,False)[0]
    half=crit/((mu/h_volume)*np.sqrt(n*p_scale*h_volume))
    return dict(estimate=f,half_width=float(half),critical=crit,lower=f-half,upper=f+half,covariance=cov)

def monotone_envelope(grid,lower,upper,query):
    grid=np.asarray(grid,float);query=np.asarray(query,float)
    lo=np.maximum.accumulate(np.clip(lower,0,1));hi=np.minimum.accumulate(np.clip(upper,0,1)[::-1])[::-1]
    if np.any(lo>hi):return np.zeros_like(query),np.ones_like(query)
    left=np.searchsorted(grid,query,side='right')-1;right=np.searchsorted(grid,query,side='left')
    a=np.zeros_like(query);b=np.ones_like(query)
    a[left>=0]=lo[left[left>=0]];b[right<len(grid)]=hi[right[right<len(grid)]]
    return a,b

def quantile_band(grid,lower,upper,probabilities):
    grid=np.asarray(grid,float);p=np.asarray(probabilities,float)
    lo=np.maximum.accumulate(np.clip(lower,0,1));hi=np.minimum.accumulate(np.clip(upper,0,1)[::-1])[::-1]
    if np.any(lo>hi):return np.full_like(p,-np.inf),np.full_like(p,np.inf)
    a=[];b=[]
    for t in p:
        ii=np.flatnonzero(hi<t);jj=np.flatnonzero(lo>=t)
        a.append(grid[ii[-1]] if len(ii) else -np.inf);b.append(grid[jj[0]] if len(jj) else np.inf)
    return np.asarray(a),np.asarray(b)
