
"""
Placeholder finite‑element solver using scikit‑fem.

Replace with a proper implicit solver for production experiments.
"""
import numpy as np

def solve_fisher_1d(D=0.1, r=2.0, K=1.0,
                    n_el=100, t_final=1.0, dt=1e-3):
    """
    Very coarse explicit Euler solver (placeholder).

    Returns
    -------
    xs : ndarray, spatial grid
    ts : ndarray, time grid
    solution : ndarray, shape (len(ts), len(xs))
    """
    print("[WARNING] FEM baseline solver not yet implemented.")
    xs = np.linspace(0, 1, n_el + 1)
    ts = np.arange(0, t_final + dt, dt)
    solution = np.zeros((len(ts), len(xs)))
    return xs, ts, solution
