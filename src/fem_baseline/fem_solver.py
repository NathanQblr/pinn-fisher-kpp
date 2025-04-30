import numpy as np
from skfem import MeshLine, Basis, asm, solve, condense
from skfem.element import ElementLineP1
from skfem.models.poisson import laplace, mass

def solve_fisher_1d(D=0.1, r=2.0, K=1.0,
                    n_el=100, t_final=1.0, dt=1e-3,
                    scheme="cn", bc_type="neumann"):
    """
    Solve Fisher-KPP in 1D with FEM in space and time-stepping.

    Parameters
    ----------
    scheme : str
        "euler" or "cn" (Crank–Nicolson)
    bc_type : str
        "dirichlet" or "neumann"

    Returns
    -------
    xs : ndarray, spatial grid
    ts : ndarray, time grid
    solution : ndarray of shape (len(ts), len(xs))
    """
    # -- FEM setup --
    mesh = MeshLine(np.linspace(0.0, 1.0, n_el + 1))
    basis = Basis(mesh, ElementLineP1())
    xs = basis.doflocs[0]

    # -- Assemble FEM matrices --
    M = asm(mass, basis)
    L = asm(laplace, basis)

    # -- Time setup --
    ts = np.arange(0, t_final + dt, dt)
    sol = np.zeros((len(ts), len(xs)))

    # -- Initial condition --
    u = np.exp(-100 * (xs - 0.5)**2)
    sol[0] = u

    # -- Boundary DOFs (only for Dirichlet) --
    if bc_type == "dirichlet":
        D_dofs = basis.get_dofs().all()
    elif bc_type == "neumann":
        D_dofs = None
    else:
        raise ValueError(f"Unknown bc_type: {bc_type}")

    # -- Time-stepping --
    if scheme == "euler":
        A = M + dt * D * L

        for i in range(1, len(ts)):
            f = r * u * (1 - u / K)
            rhs = M @ u + dt * M @ f
            if D_dofs is not None:
                A_bc, b_bc = condense(A, rhs, D=D_dofs)
                u = solve(A_bc, b_bc)
            else:
                u = solve(A, rhs)
            sol[i] = u

    elif scheme == "cn":
        A_lhs = M + 0.5 * dt * D * L
        A_rhs = M - 0.5 * dt * D * L

        for i in range(1, len(ts)):
            f = r * u * (1 - u / K)
            rhs = A_rhs @ u + dt * M @ f
            if D_dofs is not None:
                A_bc, b_bc = condense(A_lhs, rhs, D=D_dofs)
                u = solve(A_bc, b_bc)
            else:
                u = solve(A_lhs, rhs)
            sol[i] = u

    else:
        raise ValueError(f"Unknown scheme: {scheme}")

    return xs, ts, sol
