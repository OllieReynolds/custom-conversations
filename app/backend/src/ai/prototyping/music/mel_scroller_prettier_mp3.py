import numpy as np
import matplotlib.pyplot as plt
import librosa
import sounddevice as sd
import threading
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

audio_path = 'C:\\dev\\Personal\\AI\\custom-conversations\\app\\backend\\src\\ai\\prototyping\\music\\suit_up.mp3'
audio, sampling_rate = librosa.load(audio_path, sr=None, mono=True)

def audio_playback(audio, sampling_rate):
    sd.play(audio, samplerate=sampling_rate)
    sd.wait()

playback_thread = threading.Thread(target=audio_playback, args=(audio, sampling_rate))
playback_thread.start()

window_size = 4096
hop_length = 512
n_mels = 128
fmax = 8000
length_seconds = 10
length_frames = int(sampling_rate * length_seconds / hop_length)
noise_gate_threshold = -60
gain = 20

color_map = 'plasma'

fig = plt.figure(figsize=(12, 18))
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313, projection='3d')

im = ax2.imshow(np.zeros((n_mels, length_frames)), origin='lower', aspect='auto', cmap=color_map, vmin=-40, vmax=0)
ax2.set_title('Mel Spectrogram')
ax2.set_xlabel('Time [sec]')
ax2.set_ylabel('Mel bands')
plt.colorbar(im, ax=ax2, label='Decibels (dB)')

line, = ax1.plot(np.linspace(0, length_seconds, hop_length), np.zeros(hop_length), label='Waveform', color='red')
ax1.set_title('Audio Waveform')
ax1.set_xlabel('Time [sec]')
ax1.set_ylabel('Amplitude')
ax1.set_xlim(0, length_seconds)
ax1.set_ylim(-1, 1)
ax1.legend(loc='upper right')

ring_buffer = np.zeros((n_mels, length_frames))
audio_buffer = np.zeros(hop_length)
frame_idx = 0

# Adjust scatter arrays
scatter_x, scatter_y = np.meshgrid(np.linspace(0, sampling_rate / 2, n_mels), np.linspace(0, length_seconds, length_frames))
scatter_z = np.zeros(scatter_x.shape)

scatter_plot = ax3.scatter(scatter_x.flatten(), scatter_y.flatten(), scatter_z.flatten(), c=scatter_z.flatten(), cmap=color_map, depthshade=True)
ax3.set_title('3D Spectral Scatter')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Time [sec]')
ax3.set_zlabel('Magnitude')

def update_plot(frame):
    global frame_idx, ring_buffer, audio_buffer, scatter_z
    start_idx = frame_idx * hop_length
    end_idx = start_idx + hop_length
    if end_idx < len(audio):
        audio_chunk = audio[start_idx:end_idx] * gain
        max_amp = np.max(np.abs(audio_chunk))
        if max_amp > 0:
            audio_buffer[:] = audio_chunk / max_amp
        if len(audio_chunk) == hop_length:
            S = librosa.feature.melspectrogram(y=audio_chunk, sr=sampling_rate, n_mels=n_mels, n_fft=window_size, hop_length=hop_length, fmax=fmax)
            S_dB = librosa.power_to_db(S, ref=np.max)
            S_dB[S_dB < noise_gate_threshold] = noise_gate_threshold
            ring_buffer = np.roll(ring_buffer, -1, axis=1)
            ring_buffer[:, -1] = S_dB[:, 0]
            scatter_z = np.roll(scatter_z, -1, axis=0)
            scatter_z[:, -1] = S_dB
            scatter_plot._offsets3d = (scatter_x.flatten(), scatter_y.flatten(), scatter_z.flatten())
            frame_idx += 1
    im.set_data(ring_buffer)
    line.set_ydata(audio_buffer)
    scatter_plot.set_array(scatter_z.flatten())
    return [im, line, scatter_plot]

ani = FuncAnimation(fig, update_plot, blit=False, interval=1000 * hop_length / sampling_rate, repeat=True, cache_frame_data=False)

plt.show()
