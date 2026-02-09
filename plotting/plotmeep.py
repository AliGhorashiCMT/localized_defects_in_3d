import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Plot and defect-band constants
FIG_WIDTH, FIG_HEIGHT = 8, 12
Y_MIN, Y_MAX = 0.33, 0.36
DEFECT_FREQ_LO, DEFECT_FREQ_HI = 0.34, 0.35
MAX_FLATNESS_STD = 0.01

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_PATH = SCRIPT_DIR / 'data/data.dat'
OUTPUT_PATH = SCRIPT_DIR / 'data/band_structure_plot.pdf'

# Read the data file, skipping the header row
# Each row starts with "freqs:" so we need to skip that first column
data = np.loadtxt(DATA_PATH, skiprows=1, delimiter=',', usecols=range(1, 326))

# Extract the relevant columns
# Column 1 (index 0) for x-axis (k-index) - this is now index 0 after skipping "freqs:"
x_data = data[:, 0]

# Columns 7-306 (indices 6-305) for y-axis (band frequencies) - now indices 5-304
y_data_original = data[:, 5:305]  # Keep original data
y_data = data[:, 5:305]  # Working copy

# Sort frequencies for each k-point in ascending order to fix eigenvalue swapping
for i in range(y_data.shape[0]):
    y_data[i, :] = np.sort(y_data[i, :])

# Create the plot
plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))

# Plot each band with thin lines first
for i in range(y_data.shape[1]):
    plt.plot(x_data, y_data[:, i], color='gray', marker='o', markersize=3, linewidth=0.8, alpha=0.6)

# Identify the flat defect mode using the band-tracked data
# Look for bands that are relatively flat and around 0.345
defect_band_idx = None
min_flatness = float('inf')

for i in range(y_data.shape[1]):
    band_freqs = y_data[:, i]
    mean_freq = np.mean(band_freqs)
    freq_std = np.std(band_freqs)  # Standard deviation as measure of flatness
    
    # Check if this band is around 0.345 and relatively flat
    if DEFECT_FREQ_LO <= mean_freq <= DEFECT_FREQ_HI and freq_std < MAX_FLATNESS_STD:
        if freq_std < min_flatness:
            min_flatness = freq_std
            defect_band_idx = i

# Find bands immediately above and below the defect mode
adjacent_bands = []
if defect_band_idx is not None:
    defect_mean = np.mean(y_data[:, defect_band_idx])
    
    # Find the closest bands above and below
    above_band = None
    below_band = None
    min_above_diff = float('inf')
    min_below_diff = float('inf')
    
    for i in range(y_data.shape[1]):
        if i == defect_band_idx:
            continue
            
        band_mean = np.mean(y_data[:, i])
        diff = band_mean - defect_mean
        
        if diff > 0 and diff < min_above_diff:  # Band above defect
            min_above_diff = diff
            above_band = i
        elif diff < 0 and abs(diff) < min_below_diff:  # Band below defect
            min_below_diff = abs(diff)
            below_band = i
    
    if above_band is not None:
        adjacent_bands.append(above_band)
    if below_band is not None:
        adjacent_bands.append(below_band)

# Highlight the flat defect mode using original data to maintain correct tracing
if defect_band_idx is not None:
    plt.plot(x_data, y_data_original[:, defect_band_idx], color='blue', linewidth=2, label='Defect Band')

# Highlight the adjacent bands (single legend entry)
for i, idx in enumerate(adjacent_bands):
    plt.plot(x_data, y_data[:, idx], color='red', linewidth=2, label='Adjacent Bulk Band' if i == 0 else None)

# Set the frequency range focus on y-axis only
plt.ylim(Y_MIN, Y_MAX)
# Let x-axis show the full range automatically

# Add labels and title
plt.xlabel('k-index')
plt.ylabel('ω (2πc/a)')
plt.title(f'Band Structure - Frequency Range {Y_MIN} to {Y_MAX}')

# Add legend to show highlighted bands
plt.legend()

# Remove grid for cleaner look
plt.grid(False)

# Save the plot with explicit dimensions (width, height in inches)
fig = plt.gcf()
fig.set_size_inches(FIG_WIDTH, FIG_HEIGHT)
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches='tight')
plt.show()

print(f"Plot created with {y_data.shape[1]} bands")
print(f"X-axis range: {x_data.min():.4f} to {x_data.max():.4f}")
print(f"Y-axis range: {y_data.min():.4f} to {y_data.max():.4f}")
print(f"Focused Y-axis range: {Y_MIN} to {Y_MAX}")
print(f"Flat defect mode highlighted: {'Yes' if defect_band_idx is not None else 'No'}")
if defect_band_idx is not None:
    print(f"Defect mode frequency: {np.mean(y_data_original[:, defect_band_idx]):.4f} ± {np.std(y_data_original[:, defect_band_idx]):.4f}")
print(f"Adjacent bands highlighted: {len(adjacent_bands)}")
