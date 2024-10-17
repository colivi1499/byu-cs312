import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = {
    10: [0.0, 0.0, 0.0, 0.0, 0.0],
    100: [0.0002, 0.0002, 0.0002, 0.0002, 0.0002],
    1000: [0.0015, 0.0014, 0.0016, 0.0015, 0.0015],
    10000: [0.0155, 0.0152, 0.0153, 0.0157, 0.0155],
    100000: [0.1825, 0.1815, 0.1834, 0.1782, 0.1856],
    500000: [0.978, 0.9788, 0.9874, 0.9784, 0.9759],
    1000000: [2.1094, 2.0916, 2.0989, 2.0929, 2.0995]
}

df = pd.DataFrame(data)
# Data
n = np.array([10, 100, 1000, 10000, 100000, 500000, 1000000])
average_time = np.array([np.mean(times) for times in data.values()])
print(df.describe())

# Calculate n * log(n) for comparison
nlogn = n * np.log(n)

# Calculate the constant used to normalize nlogn
normalization_constant = max(average_time) / max(nlogn)
print(f"Normalization constant: {normalization_constant}")

# Normalize nlogn to make it comparable to the scale of average time
nlogn = nlogn * normalization_constant

# Create the plot
plt.figure(figsize=(8, 6))

# Plot the original data (Average Time)
plt.plot(n, average_time, marker='o', linestyle='-', color='b', label='Average Time')

# Plot n * log(n)
plt.plot(n, nlogn, marker='x', linestyle='--', color='r', label='n log(n)')

# Add titles and labels
plt.title('Average Time vs n (with n log(n) Overlay)')
plt.xlabel('n')
plt.ylabel('Time (seconds)')

# Set logarithmic scale for x-axis
plt.xscale('log')

# Show legend
plt.legend()

# Display the grid
plt.grid(True)

# Show the plot
plt.show()