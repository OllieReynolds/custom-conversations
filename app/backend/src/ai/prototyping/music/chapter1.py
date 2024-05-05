import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap

# Load an example audio file
y, sr = librosa.load(librosa.ex('trumpet'))

# Prepare the data
times = np.linspace(0, len(y) / sr, num=len(y))
points = np.array([times, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Define a linearly interpolated colormap from red to blue
cmap = LinearSegmentedColormap.from_list('interpolation', ['red', 'blue'])

# Create an array of the maximum amplitude for each segment to determine color
max_amplitude_per_segment = np.maximum(np.abs(segments[:, 0, 1]), np.abs(segments[:, 1, 1]))
norm = plt.Normalize(0, np.max(max_amplitude_per_segment))

# Create the line collection object, coloring it based on the max amplitude of each segment
lc = LineCollection(segments, cmap=cmap, norm=norm, array=max_amplitude_per_segment)
lc.set_linewidth(2)

# Plot the data
plt.figure(figsize=(12, 4))
plt.gca().add_collection(lc)
plt.xlim(times[0], times[-1])
plt.ylim(np.min(y), np.max(y))
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Waveform Colored by Segment Amplitude')
plt.colorbar(lc, label='Amplitude')

# Show the plot
plt.show()
