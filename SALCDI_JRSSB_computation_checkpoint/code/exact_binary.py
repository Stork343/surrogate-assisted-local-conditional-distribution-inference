"""Exact binomial operating characteristics for the weak-gain submodel."""
from pathlib import Path
import numpy as np,pandas as pd,json
from scipy.stats import binom,beta,norm
ROOT=Path(__file__).resolve().parents[1]

def run():
    rows=[];delta=.05;p=.1;d=.2;z=norm.ppf(.975)
    for k in [25,50,100,200,400,800,1600,3200]:
        successes=np.arange(k+1);theta_hat=successes/k-.5
        hoeff=theta_hat-np.sqrt(np.log(1/delta)/(2*k))
        cp=np.full(k+1,-.5);cp[1:]=beta.ppf(delta,successes[1:],k-successes[1:]+1)-.5
        for theta in [-.04,0.,.01,.02,.04,.06,.10,.15]:
            prob=binom.pmf(successes,k,.5+theta)
            opt=np.clip(theta/d,0,1);vstar=.25+(1-p)*(d*d*opt*opt-2*d*theta*opt)
            oracle=z*(.5-np.sqrt(vstar))
            for method,lower in [('Plug-in',theta_hat),('Hoeffding',hoeff),('Exact binomial',cp)]:
                weight=np.clip(lower/d,0,1)
                variance=.25+(1-p)*(d*d*weight*weight-2*d*theta*weight)
                gain=z*(.5-np.sqrt(variance));bad=(weight>0)&(gain < -1e-12)
                error=float(prob@bad)
                if method!='Plug-in':assert error<=delta+1e-12,(k,theta,method,error)
                rows.append(dict(k=k,theta=theta,method=method,adoption=float(prob@(weight>0)),
                                 wrong_certification=error,mean_weight=float(prob@weight),
                                 oracle_gain=float(oracle),mean_gain=float(prob@gain),
                                 mean_regret=float(prob@(oracle-gain)),scaled_signal=float(theta*np.sqrt(k))))
    frame=pd.DataFrame(rows);frame.to_csv(ROOT/'results/exact_binary.csv',index=False)
    (ROOT/'results/exact_binary_checks.json').write_text(json.dumps({'all_finite_sample_error_bounds_pass':True,'rows':len(frame),'largest_certification_error':float(frame[frame.method!='Plug-in'].wrong_certification.max()),'computed_exactly':'binomial probabilities, not simulation'},indent=2))
    print(frame[(frame.theta==0)&(frame.method=='Exact binomial')][['k','wrong_certification']].to_string(index=False))
if __name__=='__main__':run()
