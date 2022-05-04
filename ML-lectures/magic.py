import torch
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import sys

matplotlib.rcParams['figure.dpi'] = 160

# You need to clone https://github.com/NVlabs/stylegan3
sys.path.append('./stylegan3/') # because of very strange way to deserialize stylegan
import importlib.abc # fix import abc error

import dnnlib
import legacy

PET_MODEL = 'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-afhqv2-512x512.pkl'
HUMAN_MODEL = 'https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/versions/1/files/stylegan3-r-ffhq-1024x1024.pkl'


def generate_img(model, seed=None, truncation_psi=1, noise_mode='const'):
    seed = seed or np.random.randint(0, np.iinfo(np.int32).max)
    print('Loading networks from "%s"...' % model)
    device = torch.device('cuda')
    with dnnlib.util.open_url(model) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device)

    # Labels.
    label = torch.zeros([1, G.c_dim], device=device)

    # Generate images.
    print(f'Generating image for seed {seed} ...')
    z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)


    img = G(z, label, truncation_psi=truncation_psi, noise_mode=noise_mode)
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
    return img[0].cpu().numpy()


def generate_pet(seed=None):
    return generate_img(PET_MODEL, seed)


def generate_human(seed=None):
    return generate_img(HUMAN_MODEL, seed)
