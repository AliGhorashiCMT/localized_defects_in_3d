import matplotlib.pyplot as plt
import csv
import math
from collections import defaultdict
import numpy as np
from matplotlib.colors import Normalize

# Path to the CSV file
# path = '/Users/maggieshi/Desktop/SachinUROP/Plots/paper.csv'
# path2 = '/Users/maggieshi/Desktop/SachinUROP/Plots/paper1.csv'
# path = '/Users/maggieshi/Desktop/SachinUROP/Plots/eps11-1.csv'
# path2 = '/Users/maggieshi/Desktop/SachinUROP/Plots/eps11-2.csv'
# path3 = '/Users/maggieshi/Desktop/SachinUROP/Plots/eps11-3.csv'
path = '/Users/maggieshi/Desktop/SachinUROP/Plots/eps11-rand.csv'

# Indices of columns to remove
indices_to_remove = {0, 2, 4, 5, 6}

# Initialize lists
radii = []
freqs = []
q = []

# Initialize radius
radius = 0.65

for p in [path]:
    with open(p, mode='r') as file:
        csv_reader = csv.reader(file)
        
        cc = 0
        c = 1
        # Process the data rows
        for row in csv_reader:

            # Filter out unwanted columns
            filtered_row = [value for index, value in enumerate(row) if index not in indices_to_remove]
            if len(filtered_row) > 1:
                if filtered_row[0] == ' frequency':  # Check for special case if the row starts with 'frequency'
                    if cc == 6: # 6 for multiple sources
                        c += 1
                        print(radius)
                        radius += 0.0067
                        cc = 0

                    cc += 1
                else:
                    try:
                        num = float(filtered_row[1])  # Numeric value expected to be in second column after filtering
                        frq = float(filtered_row[0])
                        pred = 0.357 - 0.31372549019*(radius - 0.717)
                        if num > (10e1) and abs(frq - pred) < 0.003 and radius < 1.04:
                        # if num > 300:
                            radii.append(radius)
                            freqs.append(frq)  # Frequency value expected to be in first column after filtering
                            q.append(math.log10(num))
                    except (IndexError, ValueError):
                        # Handle cases where the row does not have enough columns or conversion fails
                        continue
        print(c)


# with open(path2, mode='r') as file:
#     csv_reader = csv.reader(file)
    
#     cc = 0
#     c = 1
#     # Process the data rows
#     for row in csv_reader:

#         # Filter out unwanted columns
#         filtered_row = [value for index, value in enumerate(row) if index not in indices_to_remove]
#         if len(filtered_row) > 1:
#             if filtered_row[0] == ' frequency':  # Check for special case if the row starts with 'frequency'
#                 if cc == 4: # 6 for multiple sources
#                     c += 1
#                     print(radius)
#                     radius += 0.0032
#                     cc = 0

#                 cc += 1
#             else:
#                 try:
#                     num = float(filtered_row[1])  # Numeric value expected to be in second column after filtering
#                     frq = float(filtered_row[0])
#                     pred = 0.344 - 0.1133*(radius - 0.7)
#                     if num > 0 and abs(frq - pred) < 0.007 and radius < 1.04:
#                     # if num > 300:
#                         radii.append(radius)
#                         freqs.append(frq)  # Frequency value expected to be in first column after filtering
#                         q.append(math.log10(num))
#                 except (IndexError, ValueError):
#                     # Handle cases where the row does not have enough columns or conversion fails
#                     continue
#     print(c)
# # Group data by radii

data_by_radius = defaultdict(list)
for r, f, q_value in zip(radii, freqs, q):
    data_by_radius[r].append((f, q_value))

# Define tolerance
tolerance = 0.003

# Initialize lists for averaged values
avg_radii = []
avg_freqs = []
avg_qs = []

# Process each radius group
for radius, values in data_by_radius.items():
    values.sort()  # Sort by frequency
    clustered_values = []
    current_cluster = []

    for i, (freq, q_value) in enumerate(values):
        if not current_cluster:
            current_cluster.append((freq, q_value))
        else:
            if abs(freq - current_cluster[-1][0]) <= tolerance:
                current_cluster.append((freq, q_value))
            else:
                clustered_values.append(current_cluster)
                current_cluster = [(freq, q_value)]
    
    if current_cluster:
        clustered_values.append(current_cluster)
    
    for cluster in clustered_values:
        avg_freq = np.mean([v[0] for v in cluster])
        avg_q = np.mean([v[1] for v in cluster])
        avg_radii.append(radius)
        avg_freqs.append(avg_freq)
        avg_qs.append(avg_q)

# Plot the data with color normalization
norm = Normalize(vmin=min(avg_qs), vmax=math.log10(10**5))
# norm = Normalize(vmin=min(q), vmax=max(q))
# plt.scatter(radii, freqs, c=q, cmap='viridis', norm=norm)
# plt.colorbar(label='Log(Q)')
# plt.xlabel('Radii')
# plt.ylabel('Frequency')
# plt.title('Scatter plot of raw data')
# plt.show()

plt.scatter(avg_radii, avg_freqs, c=avg_qs, cmap='hot', s=60, norm=norm)
plt.colorbar(label='Log(Q)')
plt.xlabel('Radii')
plt.ylabel('Frequency')
plt.title('Scatter plot of average data')
plt.savefig("rscanplot.pdf", format="pdf")
plt.show()

# plt.savefig("rscanplot.pdf", format="pdf")