
"""
Training script for the PINN.

Run:
    python -m pinn.train
"""
from pathlib import Path
import torch
from torch.optim import Adam
from torch.utils.tensorboard import SummaryWriter

from pinn.model import FCNN, physics_residual
from utils.sampling import latin_hypercube

N_INT = 5000     # interior collocation points
N_BC = 1000      # boundary points
LR = 1e-3
EPOCHS = 10000

DOMAIN = {"x": (0.0, 1.0), "t": (0.0, 1.0)}


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = FCNN().to(device)
    optim = Adam(model.parameters(), lr=LR)
    writer = SummaryWriter(log_dir="runs/pinn")

    # TODO: sample points and implement training loop
    print("[INFO] PINN skeleton created, implement training loop.")

    writer.close()


if __name__ == "__main__":
    main()
