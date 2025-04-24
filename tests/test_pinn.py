
import torch
from pinn.model import FCNN

def test_forward_shape():
    model = FCNN()
    x = torch.rand(8, 2)
    y = model(x)
    assert y.shape == (8, 1)
