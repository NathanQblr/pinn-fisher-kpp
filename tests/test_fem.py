
from fem_baseline.fem_solver import solve_fisher_1d

def test_shapes():
    xs, ts, sol = solve_fisher_1d()
    assert sol.shape == (len(ts), len(xs))
