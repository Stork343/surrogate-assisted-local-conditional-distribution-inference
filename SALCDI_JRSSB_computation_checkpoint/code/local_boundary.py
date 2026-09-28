"""Exact finite-binomial local-boundary calculations and Gaussian decision limit."""
from pathlib import Path
import numpy as np,pandas as pd
from scipy import stats,integrate
ROOT=Path(__file__).resolve().parents[1]

def run():
    rows=[];delta=.05;p=.1;d=.2;zalpha=stats.norm.ppf(.975);zd=stats.norm.ppf(1-delta)
    for k in [100,400,1600,6400,25600]:
        count=np.arange(k+1);lower=np.full(k+1,-.5)
        lower[1:]=stats.beta.ppf(delta,count[1:],k-count[1:]+1)-.5
        weight=np.clip(lower/d,0,1)
        for t in [-1.,0.,.5,1.,2.]:
            theta=t/np.sqrt(k);prob=stats.binom.pmf(count,k,.5+theta)
            var=.25+(1-p)*(d*d*weight**2-2*d*theta*weight)
            gain=zalpha*(.5-np.sqrt(var));oracle=np.clip(theta/d,0,1)
            oracle_gain=zalpha*(.5-np.sqrt(.25+(1-p)*(d*d*oracle**2-2*d*theta*oracle)))
            # Squared-loss expression is exact for the limiting decision rule,
            # including the one-sided null boundary.
            def regret(z):
                a=max(0.,t+.5*z-.5*zd)
                return zalpha*(1-p)*(max(t,0.)**2-2*t*a+a*a)*stats.norm.pdf(z)
            limit=integrate.quad(regret,-10,10,epsabs=1e-10,points=[zd-2*t])[0]
            rows.append(dict(k=k,local_parameter=t,theta=theta,
                adoption=float(prob@(weight>0)),limit_adoption=float(stats.norm.sf(zd-2*t)),
                harmful_certification=float(prob@(gain< -1e-12)),
                scaled_mean_regret=float(k*(oracle_gain-prob@gain)),limit_scaled_mean_regret=limit))
    pd.DataFrame(rows).to_csv(ROOT/'results/local_boundary.csv',index=False)
    print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':run()
