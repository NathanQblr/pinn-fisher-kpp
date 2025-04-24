
"""
Sampling utilities.
"""
import torch


def latin_hypercube(n_samples: int, dim: int, low=0.0, high=1.0):
    """Generate Latin‑Hypercube samples."""
    cut = torch.linspace(0, 1, n_samples + 1)[:-1]
    u = torch.rand(n_samples, dim)
    a = cut + u / n_samples
    samples = a[torch.randperm(n_samples)]
    return samples * (high - low) + low
