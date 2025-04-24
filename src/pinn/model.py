
"""
Physics‑Informed Neural Network module.

Implements a simple fully‑connected network and placeholders for the physics residuals
of the 1‑D Fisher–KPP reaction–diffusion equation.

Usage
-----
>>> from pinn.model import FCNN, physics_residual
"""

import torch
import torch.nn as nn


class FCNN(nn.Module):
    """Fully‑connected network with Tanh activations."""
    def __init__(self, in_dim: int = 2, hidden: int = 64,
                 depth: int = 5, out_dim: int = 1):
        super().__init__()
        layers = [nn.Linear(in_dim, hidden), nn.Tanh()]
        for _ in range(depth - 1):
            layers += [nn.Linear(hidden, hidden), nn.Tanh()]
        layers += [nn.Linear(hidden, out_dim)]
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


def physics_residual(model: nn.Module, x_t: torch.Tensor,
                     D: float = 0.1, r: float = 2.0, K: float = 1.0):
    """
    Compute PDE residual ∂_t u − D ∂_{xx} u − r u (1 − u/K)
    for collocation points x_t = (x, t).

    Parameters
    ----------
    model : nn.Module
        The neural network approximating u(x,t).
    x_t : Tensor
        Collocation points of shape (N, 2), columns (x,t) **requires_grad=True**.
    D, r, K : float
        Equation parameters.

    Returns
    -------
    Tensor
        Residual values for each collocation point.
    """
    raise NotImplementedError("Define autograd computations here.")
