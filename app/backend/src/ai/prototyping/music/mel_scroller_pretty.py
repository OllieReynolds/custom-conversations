import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import librosa
from matplotlib.animation import FuncAnimation
import threading

# Parameters
window_size = 4096
hop_length = 256
n_mels = 256
fmax = 8000
sampling_rate = 44100
length_seconds = 1
length_frames = int(sampling_rate * length_seconds / hop_length)
noise_gate_threshold = -50

# Initialize the plot with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
im = ax2.imshow(np.zeros((n_mels, length_frames)), origin='lower', aspect='auto', cmap='viridis', vmin=-60, vmax=0)
ax2.set_title('Real-time Mel Spectrogram')
ax2.set_xlabel('Time [sec]')
ax2.set_ylabel('Frequency [Hz]')
plt.colorbar(im, ax=ax2, label='Decibels (dB)')

# Setup for waveform display
line, = ax1.plot(np.linspace(0, length_seconds, hop_length), np.zeros(hop_length), label='Waveform')
ax1.set_xlim(0, length_seconds)
ax1.set_ylim(-1, 1)
ax1.legend(loc='upper right')

# Ring buffer for the spectrogram
ring_buffer = np.zeros((n_mels, length_frames))
audio_buffer = np.zeros(hop_length)

def update_plot(frame):
    im.set_data(ring_buffer)
    line.set_ydata(audio_buffer)
    return [im, line]

def audio_callback(indata, frames, time, status):
    global ring_buffer, audio_buffer
    audio_buffer = indata[:, 0]
    if np.max(indata) < 0.01:
        ax2.set_title('Real-time Mel Spectrogram - Noise gate active')
        return
    ax2.set_title('Real-time Mel Spectrogram')
    S = librosa.feature.melspectrogram(y=indata[:, 0], sr=sampling_rate, n_mels=n_mels, n_fft=window_size, hop_length=hop_length, fmax=fmax)
    S_dB = librosa.power_to_db(S, ref=np.max)
    S_dB[S_dB < noise_gate_threshold] = -80
    ring_buffer = np.roll(ring_buffer, -1, axis=1)
    ring_buffer[:, -1] = S_dB[:, 0]

def audio_stream():
    with sd.InputStream(callback=audio_callback, blocksize=hop_length, channels=1, samplerate=sampling_rate):
        while True:
            sd.sleep(1000)

thread = threading.Thread(target=audio_stream)
thread.start()

ani = FuncAnimation(fig, update_plot, blit=True, interval=1000 * hop_length / sampling_rate, repeat=True, cache_frame_data=False)

plt.show()
