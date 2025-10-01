# src/model.py
from scipy.stats import norm
import numpy as np

def prob_in_bracket(S, A, B, sigma, tau):
    """
    Compute probability that the S&P closes in [A,B] using Normal distribution.

    Parameters
    ----------
    S : float
        Current S&P price
    A : float
        Lower bracket bound
    B : float
        Upper bracket bound
    sigma : float
        Daily volatility (e.g., 0.01 * S for 1% daily vol)
    tau : float
        Fraction of the trading day left (e.g., 0.25 = 1.5 hrs if 6.5 hr day)

    Returns
    -------
    float
        Probability (between 0 and 1)
    """
    z_hi = (B - S) / (sigma * np.sqrt(tau))
    z_lo = (A - S) / (sigma * np.sqrt(tau))
    return norm.cdf(z_hi) - norm.cdf(z_lo)
