"""Audit numerical integration without changing the frozen statistical protocol."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import json
import numpy as np,pandas as pd
from simulation import prepare,default_cells,truth_and_covariance
from paired_band import *
ROOT=Path(__file__).resolve().parents[1]

def run():
    cfg=json.loads((ROOT/'results/main/manifest.json').read_text())['config']
    wg=np.linspace(0,1,cfg['weight_count']);rows=[]
    for cid in [1,2,4,7,8,9]:
        cell=next(c for c in default_cells() if c['id']==cid)
        for rep in range(10):
            z=prepare(cell,rep,cfg);ii=z['gi'];h=cfg['bandwidth'];p=cell['p']
            gate=local_moments(z['u'][ii],z['b'][ii],z['k'][ii],z['r'][ii],p_scale=p,h_volume=h)
            comparisons=[]
            for draws in [2048,16384]:
                it=RadialGaussian(spherical_directions(cfg['thresholds'],draws,7241))
                comparisons.append(paired_calibration(gate,it,wg,delta=cfg['delta'],multiplier_draws=cfg['multipliers'],seed=z['seed']+71,remainder=cfg['remainder']))
            a,b=comparisons
            _,om1=truth_and_covariance(z['qf'],z['mf'],p,cell['scenario'],cell['design'],h,z['thresholds'])
            _,om2=truth_and_covariance(z['qf'],z['mf'],p,cell['scenario'],cell['design'],h,z['thresholds'],nx=96,ns=64)
            rows.append(dict(cell_id=cid,replicate=rep,weight_2048=a['weight'],weight_16384=b['weight'],
                             same_weight=a['weight']==b['weight'],max_critical_error=float(abs(a['critical_values']-b['critical_values']).max()),
                             max_gain_error=float(abs(a['gains']-b['gains']).max()),radius_error=abs(a['slope_radius']-b['slope_radius']),
                             truth_covariance_error=float(abs(om1-om2).max())))
    df=pd.DataFrame(rows);df.to_csv(ROOT/'results/numerical_audit.csv',index=False)
    result=dict(replications=len(df),selection_agreement=float(df.same_weight.mean()),max_critical_difference=float(df.max_critical_error.max()),
                max_gain_difference=float(df.max_gain_error.max()),max_truth_covariance_difference=float(df.truth_covariance_error.max()),
                interpretation='Convergence assessment, not a rigorous uniform quadrature certificate')
    (ROOT/'results/numerical_audit.json').write_text(json.dumps(result,indent=2));print(result)
if __name__=='__main__':run()
