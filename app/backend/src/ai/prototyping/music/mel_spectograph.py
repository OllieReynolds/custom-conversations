import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd
import librosa

# Parameters
window_size = 2048  # Size of the FFT window
hop_length = 512   # Number of samples between successive frames
n_mels = 128       # Number of Mel bands
fmax = 8000        # Maximum frequency
sampling_rate = 44100  # Audio sampling rate

# Initialize the plot
fig, ax = plt.subplots()
S_dB = np.zeros((n_mels, int(np.ceil(window_size / hop_length))))
im = ax.imshow(S_dB, origin='lower', aspect='auto', cmap='viridis', vmin=-80, vmax=0)
ax.set_title('Real-time Mel Spectrogram')
ax.set_xlabel('Time')
ax.set_ylabel('Frequency')
plt.colorbar(im, ax=ax)

def update_plot(frame):
    im.set_data(S_dB)
    return [im]

def audio_callback(indata, frames, time, status):
    """This function is called for each audio block from the microphone."""
    S = librosa.feature.melspectrogram(y=indata[:, 0], sr=sampling_rate, n_mels=n_mels, n_fft=window_size, hop_length=hop_length, fmax=fmax)
    global S_dB
    S_dB = librosa.power_to_db(S, ref=np.max)
    S_dB = np.roll(S_dB, -1, axis=1)  # Shift the spectrogram to the left
    S_dB[:, -1] = librosa.power_to_db(S[:, -1], ref=np.max)  # Update the latest column with new data

# Set up the sound device stream
stream = sd.InputStream(callback=audio_callback, blocksize=hop_length, channels=1, samplerate=sampling_rate)

# Use FuncAnimation to update the plot smoothly
ani = FuncAnimation(fig, update_plot, blit=True, interval=1000 * hop_length / sampling_rate, save_count=50)

with stream:
    plt.show()
