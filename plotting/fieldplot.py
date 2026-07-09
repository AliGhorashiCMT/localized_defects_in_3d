import os
import h5py
import numpy as np
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
h5_file = os.path.join(SCRIPT_DIR, "data", "rscan-2-ez-001134.28.h5")
dataset_name = "ez"
z_index = 200  # Change this to select a different z slice

with h5py.File(h5_file, 'r', locking=False) as f:
    data = f[dataset_name][:]
    xy_slice = data[:, z_index, :]  # Slicing at z_index


plt.imshow(xy_slice, aspect='auto', cmap='seismic')
plt.colorbar(label='Value')
plt.title(f'2D Colormap of {dataset_name} at z={z_index}')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig(os.path.join(SCRIPT_DIR, "fieldplot.pdf"), format="pdf")
plt.show()
