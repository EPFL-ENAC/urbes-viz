import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# Directory to save PNGs
output_dir = 'output_images_u10'
os.makedirs(output_dir, exist_ok=True)

# List of WRF output files
wrf_files = sorted([os.path.join('data', f) for f in os.listdir('data') if f.startswith('wrfout_d01')])

for i, file in enumerate(wrf_files):
    with h5py.File(file, 'r') as hdf_file:
        temperature = hdf_file['U10'][0, :, :]
        temperature_flipped = np.flipud(temperature)

        plt.figure(figsize=(10, 6))
        plt.imshow(temperature_flipped, cmap='viridis')
        plt.axis('off')
        plt.savefig(os.path.join(output_dir, f'u10_{i:03d}.png'), bbox_inches='tight', pad_inches=0)
        plt.close()