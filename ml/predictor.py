import torch
from model import AIMModel

model = AIMModel()
model.load_state_dict(torch.load("aim_model.pt"))
model.eval()

def predict(input_tensor):
    return model(input_tensor).detach().numpy()
