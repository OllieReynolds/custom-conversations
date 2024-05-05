import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import librosa
from matplotlib.animation import FuncAnimation
import threading

# Parameters
window_size = 2048
hop_length = 512
n_mels = 128
fmax = 8000
sampling_rate = 44100
length_seconds = 1
length_frames = int(sampling_rate * length_seconds / hop_length)

# Initialize the plot
fig, ax = plt.subplots(figsize=(12, 4))
im = ax.imshow(np.zeros((n_mels, length_frames)), origin='lower', aspect='auto', cmap='viridis', extent=[0, length_seconds, 0, fmax], vmin=-80, vmax=0)
ax.set_title('Real-time Mel Spectrogram')
ax.set_xlabel('Time [sec]')
ax.set_ylabel('Frequency [Hz]')
plt.colorbar(im, ax=ax)

# Ring buffer to hold the incoming audio frames
ring_buffer = np.zeros((n_mels, length_frames))

def update_plot(frame):
    im.set_data(ring_buffer)
    return [im]

def audio_callback(indata, frames, time, status):
    global ring_buffer
    S = librosa.feature.melspectrogram(y=indata[:, 0], sr=sampling_rate, n_mels=n_mels, n_fft=window_size, hop_length=hop_length, fmax=fmax)
    S_dB = librosa.power_to_db(S, ref=np.max)
    ring_buffer = np.roll(ring_buffer, -1, axis=1)
    ring_buffer[:, -1] = S_dB[:, 0]

def audio_stream():
    with sd.InputStream(callback=audio_callback, blocksize=hop_length, channels=1, samplerate=sampling_rate):
        while True:
            sd.sleep(1000)

# Run the audio stream in a separate thread
thread = threading.Thread(target=audio_stream)
thread.start()

# Animation update function
ani = FuncAnimation(fig, update_plot, blit=True, interval=1000 * hop_length / sampling_rate, repeat=True)

plt.show()
