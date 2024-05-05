# Load Libraries
import numpy as np
import matplotlib.pyplot as plt
import librosa
import sounddevice as sd
import threading
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D

# Load Audio
audio_path = 'C:\\dev\\Personal\\AI\\custom-conversations\\app\\backend\\src\\ai\\prototyping\\music\\wake_me_up.mp3'
audio, sampling_rate = librosa.load(audio_path, sr=None, mono=True)

# Playback Function
def audio_playback(audio, sampling_rate):
    sd.play(audio, samplerate=sampling_rate)
    sd.wait()

# Start Playback in a Thread
playback_thread = threading.Thread(target=audio_playback, args=(audio, sampling_rate))
playback_thread.start()

# Set Parameters
window_size = 2048  # Reduced window size to match hop length
hop_length = 512
n_mels = 128
fmax = 8000
length_seconds = 10
length_frames = int(sampling_rate * length_seconds / hop_length)
noise_gate_threshold = -60
gain = 20

# Setup Plot
fig = plt.figure(figsize=(15, 20))
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313, projection='3d')

# Initial Plotting Setup
im = ax2.imshow(np.zeros((n_mels, length_frames)), origin='lower', aspect='auto', cmap='plasma', vmin=-40, vmax=0)
ax2.set_title('Mel Spectrogram')
ax2.set_xlabel('Time [sec]')
ax2.set_ylabel('Frequency [Hz]')
plt.colorbar(im, ax=ax2, label='Decibels (dB)')

# Waveform and FFT Plots
line, = ax1.plot(np.linspace(0, length_seconds, hop_length), np.zeros(hop_length), label='Waveform', color='red')
ax1.set_xlim(0, length_seconds)
ax1.set_ylim(-1.1, 1.1)
ax1.legend(loc='upper right')

# Buffers for Audio Data
ring_buffer = np.zeros((n_mels, length_frames))
audio_buffer = np.zeros(hop_length)
frame_idx = 0
current_time_overlay = ax2.add_patch(Rectangle((0, 0), 1, n_mels, color='white', alpha=0.3))

# Update Function for Animation
def update_plot(frame):
    global frame_idx, ring_buffer, audio_buffer
    start_idx = frame_idx * hop_length
    end_idx = start_idx + hop_length
    if end_idx < len(audio):
        audio_chunk = audio[start_idx:end_idx] * gain
        audio_buffer[:] = audio_chunk
        if len(audio_chunk) == hop_length:
            S = librosa.feature.melspectrogram(y=audio_chunk, sr=sampling_rate, n_mels=n_mels, n_fft=window_size, hop_length=hop_length, fmax=fmax)
            S_dB = librosa.power_to_db(S, ref=np.max)
            S_dB[S_dB < noise_gate_threshold] = noise_gate_threshold
            ring_buffer = np.roll(ring_buffer, -1, axis=1)
            ring_buffer[:, -1] = S_dB[:, 0]
            frame_idx += 1
    im.set_data(ring_buffer)
    line.set_ydata(audio_buffer)
    current_time_overlay.set_xy((length_frames - frame_idx % length_frames, 0))
    ax3.clear()
    # Create the meshgrid for X, Y
    X, Y = np.meshgrid(np.linspace(0, length_seconds, ring_buffer.shape[1]), np.linspace(0, fmax, n_mels))
    # Plot using X, Y, and ring_buffer (without transposing it)
    ax3.plot_surface(X, Y, ring_buffer, cmap='plasma')
    return [im, line, current_time_overlay, ax3]

# Run Animation
ani = FuncAnimation(fig, update_plot, blit=True, interval=1000 * hop_length / sampling_rate, repeat=True, cache_frame_data=False)
plt.show()
