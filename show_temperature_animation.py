import h5py
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import os
from matplotlib.animation import FuncAnimation

# Define the directory containing your WRF output files
data_dir = 'data_folder/wrf'

# List of all WRF output files
wrf_files = sorted([os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.startswith('wrfout_d01')])

# Initialize lists to store data
time_series = []

# Loop through each file and extract temperature data
for file in wrf_files:
    with h5py.File(file, 'r') as hdf_file:
        temperature = hdf_file['T2'][0, :, :]  # Extract the first time step's temperature
        time_series.append(temperature)

# Get the coordinates for plotting (assuming they are the same across all files)
with h5py.File(wrf_files[0], 'r') as hdf_file:
    longitude = hdf_file['XLONG'][0, :, :]
    latitude = hdf_file['XLAT'][0, :, :]

# Set up the plot
fig, ax = plt.subplots()
cax = ax.pcolormesh(longitude, latitude, time_series[0], shading='auto', cmap='plasma')
fig.colorbar(cax, ax=ax, label='Temperature (K)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Surface Temperature Evolution')

# Function to update the plot for each frame
def update(frame):
    ax.clear()
    cax = ax.pcolormesh(longitude, latitude, time_series[frame], shading='auto', cmap='plasma')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Surface Temperature on {wrf_files[frame].split("_")[-2]}')

# Create the animation
anim = FuncAnimation(fig, update, frames=len(time_series), repeat=True)

# Show the animation
plt.show()