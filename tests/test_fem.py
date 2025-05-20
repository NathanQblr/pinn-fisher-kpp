import numpy as np
from fem_baseline.fem_solver import solve_fisher_1d


def test_shapes():
    xs, ts, sol = solve_fisher_1d()
    assert sol.shape == (len(ts), len(xs))

def test_fisher_neumann_runs():
    from fem_baseline.fem_solver import solve_fisher_1d

    xs, ts, sol = solve_fisher_1d(bc_type="neumann", t_final=0.1)
    assert sol.shape == (len(ts), len(xs))
    assert np.all(sol >= 0.0) and np.all(sol <= 1.0)
