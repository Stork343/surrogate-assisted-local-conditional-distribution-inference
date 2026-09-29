#!/usr/bin/env python3
"""Reproduce the core calculations for paired certification of local CDF bands.

Dependencies: numpy, scipy. No network access or input data are required.
Run: python verify_core.py --output verification_results.json

This is a verification/prototype module, not the complete revised empirical pipeline.
The covariance confidence radius is a conservative, explicit Bernstein construction.
No numerical local optimizer is used as if it certified a global robust minimum.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import norm, beta, binom


def covariance_example(p: float = 0.1) -> np.ndarray:
    """Exact finite-support E[(sqrt(p)*(U0-F),sqrt(p)*B) outer product]."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be strictly between zero and one")
    q = np.array([0.1, 0.5])
    thresholds = np.array([0.0, 1.0])
    omega = np.zeros((4, 4))
    mean = np.zeros(4)
    for s, y, mass in [(0, 1, .4), (0, 2, .4), (1, 0, .1), (1, 2, .1)]:
        z = (y <= thresholds).astype(float)
        m = np.array([.5 * s, .5 + .4 * (s - .2)])
        assert np.all(np.diff(m) >= 0) and np.all((m >= 0) & (m <= 1))
        for r, rp in [(0, 1 - p), (1, p)]:
            a = (r / p) * (z - q)
            b = (1 - r / p) * (m - q)
            v = np.sqrt(p) * np.r_[a, b]
            mean += mass * rp * v
            omega += mass * rp * np.outer(v, v)
    if not np.allclose(mean, 0., atol=1e-14):
        raise AssertionError("The scores were not correctly centered")
    return omega


def path_covariance(omega: np.ndarray, weight: float) -> np.ndarray:
    omega = np.asarray(omega, dtype=float)
    if omega.ndim != 2 or omega.shape[0] != omega.shape[1] or omega.shape[0] % 2:
        raise ValueError("omega must be an even-dimensional square matrix")
    if not 0.0 <= weight <= 1.0:
        raise ValueError("weight must be in [0,1]")
    j = omega.shape[0] // 2
    h = np.c_[np.eye(j), weight * np.eye(j)]
    ans = h @ omega @ h.T
    return (ans + ans.T) / 2


def rectangle_probability(c: float, sigma: np.ndarray) -> float:
    """Deterministic Gaussian rectangle integration for J=1 or J=2."""
    sigma = np.asarray(sigma, dtype=float)
    if c < 0:
        return 0.0
    if sigma.shape == (1, 1):
        v = float(sigma[0, 0])
        if v <= 0:
            return 1.0 if v == 0 else float("nan")
        return float(2 * norm.cdf(c / np.sqrt(v)) - 1)
    if sigma.shape != (2, 2):
        raise ValueError("This deterministic verification routine supports only J=1 or J=2")
    if np.linalg.eigvalsh(sigma)[0] <= 0:
        raise ValueError("Bivariate numerical routine requires positive definite sigma")
    s1 = np.sqrt(sigma[0, 0])
    slope = sigma[1, 0] / sigma[0, 0]
    cond_sd = np.sqrt(sigma[1, 1] - sigma[1, 0] ** 2 / sigma[0, 0])
    def integrand(x: float) -> float:
        return float(norm.pdf(x, scale=s1) * (
            norm.cdf((c - slope*x) / cond_sd) - norm.cdf((-c - slope*x) / cond_sd)))
    val, err = quad(integrand, -c, c, epsabs=1e-11, epsrel=1e-11, limit=100)
    if err > 1e-8:
        raise ArithmeticError("Quadrature error exceeded the verification tolerance")
    return float(val)


def critical_value(sigma: np.ndarray, alpha: float = 0.05) -> float:
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0,1)")
    upper = max(1.0, 5*np.sqrt(float(np.diag(sigma).max())))
    while rectangle_probability(upper, sigma) < 1-alpha:
        upper *= 2
    return float(brentq(lambda c: rectangle_probability(c, sigma)-(1-alpha),
                        0.0, upper, xtol=1e-11))


def critical_gain(omega: np.ndarray, weight: float, alpha: float = .05) -> float:
    if weight == 0:
        return 0.0  # Preserve the exact paired anchor identity.
    return critical_value(path_covariance(omega, 0), alpha) - critical_value(
        path_covariance(omega, weight), alpha)


def covariance_certificate(
    kernel: np.ndarray, y: np.ndarray, verified: np.ndarray, propensity: np.ndarray,
    anchor: np.ndarray, surrogate: np.ndarray, thresholds: np.ndarray, *,
    p: float, h_volume: float, e_lower: float, kernel_bound: float = 1.,
    delta: float = .05,
) -> dict[str, Any]:
    """Explicit confidence ball for the scaled joint second moment in the note.

    Assumptions are part of the contract: iid selection observations independent
    of training; known propensity >= p*e_lower globally on kernel support;
    deterministic h_volume=h**d; bounded nonnegative kernel; candidate CDF values
    in [0,1]. Unverified y may be NaN. No assumption of correct candidate models.
    The radius is conservative; no claim of sharp finite-sample constants is made.
    """
    k = np.asarray(kernel, float); y = np.asarray(y, float)
    r = np.asarray(verified, bool); pi = np.asarray(propensity, float)
    q = np.asarray(anchor, float); m = np.asarray(surrogate, float)
    thresholds = np.asarray(thresholds, float)
    n = len(k); j = len(thresholds); ell = 2*j+1
    if n < 2 or j < 1 or q.shape != (n,j) or m.shape != (n,j):
        raise ValueError("Incompatible dimensions, fewer than two rows, or no thresholds")
    if any(v.shape != (n,) for v in (y,r,pi)):
        raise ValueError("Row arrays must have common length")
    if not (0 < p <= 1 and h_volume > 0 and e_lower > 0 and 0 < delta < 1):
        raise ValueError("Invalid scale or confidence parameters")
    if (np.any(~np.isfinite(k)) or np.any(k < 0) or np.any(k > kernel_bound)
        or np.any(~np.isfinite(pi)) or np.any(pi <= 0) or np.any(pi > 1)
        or np.any(pi + 1e-14 < p*e_lower)):
        raise ValueError("Kernel or propensity bounds violated")
    if np.any(~np.isfinite(y[r])):
        raise ValueError("Verified outcomes must be finite")
    if (np.any(~np.isfinite(q)) or np.any(~np.isfinite(m))
        or np.any((q < 0)|(q > 1)) or np.any((m < 0)|(m > 1))):
        raise ValueError("Candidate functions must be finite and in [0,1]")
    u = q.copy()
    u[r] += ((y[r,None] <= thresholds).astype(float) - q[r]) / pi[r,None]
    b = (1 - r.astype(float)/pi)[:,None] * (m-q)
    muhat = float(k.mean())
    fhat = np.clip(np.mean(k[:,None]*u, axis=0)/muhat,0,1) if muhat > 0 else np.full(j,.5)
    raw = np.c_[k, k[:,None]*u, k[:,None]*b] * np.sqrt(p/h_volume)
    qhat = raw.T @ raw / n
    transform = np.zeros((2*j,ell))
    transform[:j,0] = -fhat
    transform[:j,1:1+j] = np.eye(j)
    transform[j:,1+j:] = np.eye(j)
    omegahat = transform @ qhat @ transform.T
    dpart = delta/4
    count = int(np.count_nonzero(k))
    mass_upper = float(beta.ppf(1-dpart,count+1,n-count)) if count < n else 1.
    v_upper = mass_upper/h_volume
    tq = np.log(2*ell*ell/dpart); tn = np.log(2*j/dpart); tm = np.log(2/dpart)
    mx = kernel_bound/(e_lower*np.sqrt(p*h_volume))
    vq = 2*kernel_bound**4*v_upper/(p*e_lower**3*h_volume)
    rq = np.sqrt(2*vq*tq/n) + 4*mx*mx*tq/(3*n)
    vn = 2*kernel_bound**2*mass_upper/(p*e_lower)
    rn = np.sqrt(2*vn*tn/n)+4*kernel_bound*tn/(3*n*p*e_lower)
    vm = kernel_bound**2*mass_upper
    rm = np.sqrt(2*vm*tm/n)+2*kernel_bound*tm/(3*n)
    zeta = min(1.,(rn+rm)/muhat) if muhat > 0 else 1.
    qnorm_upper = float(np.linalg.norm(qhat,2)+ell*rq)
    epsilon = (j+1)*ell*rq + 2*np.sqrt(j*(j+1))*zeta*qnorm_upper
    return {"omega_hat":omegahat,"epsilon":float(epsilon),"F_pilot":fhat,
            "centering_radius":float(zeta),"kernel_mass_upper":mass_upper,
            "kernel_support":count,"verified_kernel_support":int(np.sum(r & (k>0))),
            "delta":delta,"n_selection":n,"N_selection":float(n*p*h_volume)}


def scalar_variance(theta: float, weight: float, p: float=.1, d: float=.2) -> float:
    return .25 + (1-p)*(weight*weight*d*d-2*weight*d*theta)


def scalar_certified_weight(theta_hat: float, k: int, delta: float=.05,
                            d: float=.2) -> tuple[float, float]:
    if k <= 0:
        return 0., float("-inf")
    lower = theta_hat - np.sqrt(np.log(1/delta)/(2*k))
    weight = float(np.clip(lower/d,0.,1.))
    return weight, float(lower)


def exact_scalar_adoption_probability(theta: float, k: int, delta: float=.05) -> float:
    """Conditional on k labels, V=S(2Z-1), P(V=1)=.5+theta."""
    threshold = k*(.5+np.sqrt(np.log(1/delta)/(2*k)))
    # Strict lower confidence bound > 0; adoption iff binomial count > threshold.
    cutoff = int(np.floor(threshold))
    return float(binom.sf(cutoff,k,.5+theta))


def run_verifications() -> dict[str, Any]:
    omega = covariance_example()
    a = omega[:2,:2]; c = omega[:2,2:] + omega[2:,:2]; v = omega[2:,2:]
    liv = float(-np.trace(c)/(2*np.trace(v)))
    opt = minimize_scalar(lambda l: critical_value(path_covariance(omega,float(l))),
                          bounds=(0,1),method="bounded",options={"xatol":1e-9})
    rows=[]
    for name, l in [("Anchor",0.),("Integrated variance",liv),
                    ("Band critical value",float(opt.x)),("Full",1.)]:
        sigma=path_covariance(omega,l)
        rows.append({"rule":name,"weight":l,"trace":float(np.trace(sigma)),
                     "critical_95":critical_value(sigma),"covariance":sigma.tolist()})
    assert np.isclose(liv,25/41)
    assert rows[1]["trace"] < rows[0]["trace"]
    assert rows[1]["critical_95"] > rows[0]["critical_95"]
    assert rows[2]["critical_95"] < rows[0]["critical_95"]
    anchor_union=float(2*norm.sf(.99/.3)+2*norm.sf(.99/.5))
    iv_upper=float(2*norm.cdf(.99/np.sqrt(path_covariance(omega,liv)[1,1]))-1)
    assert anchor_union < .05 and iv_upper < .95
    perturb=.001; perturbed=omega+perturb*np.eye(4)
    paired=[]
    for l in [0.,1e-4,1e-3,.01,.1,.5,1.]:
        err=abs(critical_gain(perturbed,l)-critical_gain(omega,l))
        paired.append({"weight":l,"paired_error":err,
                       "error_over_weight_times_perturbation":err/(l*perturb) if l>0 else None})
    assert paired[0]["paired_error"] == 0
    theta_rows=[]
    for k in [100,400,1600]:
        assert exact_scalar_adoption_probability(0.,k) <= .05+1e-12
        for theta in [0.,.03,.06,.12]:
            lstar=min(max(theta/.2,0),1)
            gain=norm.ppf(.975)*(.5-np.sqrt(scalar_variance(theta,lstar)))
            theta_rows.append({"local_verified_k":k,"theta":theta,
                               "oracle_weight":lstar,"oracle_critical_gain":float(gain),
                               "exact_adoption_probability":exact_scalar_adoption_probability(theta,k)})
    # Check deterministic safety on every possible observed count for selected theta values.
    for theta in [-.10,0.,.03,.12,.24]:
        for k in [40,100,400]:
            for successes in range(k+1):
                that=successes/k-.5
                l,lower=scalar_certified_weight(that,k)
                if lower <= theta and l>0:
                    assert scalar_variance(theta,l) < .25+1e-13
    # Smoke test the observable Bernstein confidence-ball implementation.
    rng=np.random.default_rng(20260927); n=20000;p=.1
    s=rng.binomial(1,.2,n);coin=rng.binomial(1,.5,n)
    y=np.where(s==0,np.where(coin==0,1.,2.),np.where(coin==0,0.,2.))
    r=rng.binomial(1,p,n).astype(bool); observed_y=np.where(r,y,np.nan)
    q=np.tile([.1,.5],(n,1));m=np.c_[.5*s,.5+.4*(s-.2)]
    cert=covariance_certificate(np.ones(n),observed_y,r,np.full(n,p),q,m,
                                np.array([0.,1.]),p=p,h_volume=1.,e_lower=1.)
    observed_error=float(np.linalg.norm(cert["omega_hat"]-omega,2))
    assert observed_error <= cert["epsilon"]
    cert_serial={k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in cert.items()}
    cert_serial["realized_operator_error_in_smoke_test"]=observed_error
    cert_serial["interpretation"]="One smoke test, not a Monte Carlo estimate of confidence coverage; radius intentionally conservative."
    return {"seed":20260927,"numpy_version":np.__version__,"scipy_version":scipy.__version__,
            "omega_exact":omega.tolist(),"separation":rows,
            "analytic_separation_at_c_0_99":{"anchor_union_tail_upper":anchor_union,
              "IV_second_coordinate_coverage_upper":iv_upper},
            "paired_perturbation_checks":paired,"scalar_certification":theta_rows,
            "covariance_certificate_smoke_test":cert_serial,
            "all_assertions_passed":True}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("verification_results.json"))
    args=parser.parse_args()
    result=run_verifications()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"all_assertions_passed":True,"separation":result["separation"],
                      "output":str(args.output)},indent=2))

if __name__ == "__main__":
    main()
