import numpy as np
import matplotlib.pyplot as plt
import librosa
import sounddevice as sd
import threading
from matplotlib.animation import FuncAnimation

# Load the audio file
audio_path = 'C:\\dev\\Personal\\AI\\custom-conversations\\app\\backend\\src\\ai\\prototyping\\music\\nights.mp3'
audio, sampling_rate = librosa.load(audio_path, sr=None, mono=True)

# Define parameters
window_size = 4096
hop_length = 512
n_mels = 128
fmax = 8000
noise_gate_threshold = -60
gain = 20
fft_points = window_size

# Calculate the number of frames needed
total_frames = (len(audio) // hop_length) + (1 if len(audio) % hop_length else 0)

# Initialize data arrays
spectrogram_data = np.zeros((n_mels, total_frames))
waveform_data = np.zeros(total_frames)
fft_magnitude_data = np.zeros((fft_points // 2 + 1, total_frames))

# Precompute all frames
for i in range(total_frames):
    start_idx = i * hop_length
    end_idx = start_idx + hop_length
    if end_idx > len(audio):
        audio_chunk = np.zeros(hop_length)  # Pad last chunk with zeros
    else:
        audio_chunk = audio[start_idx:end_idx]

    audio_chunk *= gain  # Apply gain
    S = librosa.feature.melspectrogram(y=audio_chunk, sr=sampling_rate, n_mels=n_mels, n_fft=window_size, hop_length=hop_length, fmax=fmax)
    S_dB = librosa.power_to_db(S, ref=np.max)
    S_dB[S_dB < noise_gate_threshold] = noise_gate_threshold
    if S_dB.shape[0] != n_mels:
        raise ValueError(f"Expected mel spectrogram to have {n_mels} rows, got {S_dB.shape[0]}")
    spectrogram_data[:, i] = S_dB.mean(axis=1)

# Prepare the matplotlib figure and axes
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

# Initialize plots
im = ax2.imshow(spectrogram_data, aspect='auto', origin='lower', interpolation='none', cmap='plasma', vmin=-40, vmax=0)
ax2.set_title('Mel Spectrogram')
ax2.set_xlabel('Time [sec]')
ax2.set_ylabel('Mel bands')

line, = ax1.plot(np.linspace(0, len(audio) / sampling_rate, total_frames), np.zeros(total_frames), color='red')
ax1.set_ylim(-1, 1)
ax1.set_title('Audio Waveform')
ax1.set_xlabel('Time [sec]')
ax1.set_ylabel('Amplitude')

fft_freqs = np.linspace(0, sampling_rate / 2, fft_points // 2 + 1)
fft_line, = ax3.plot(fft_freqs, np.zeros_like(fft_freqs), color='blue')
ax3.set_ylim(0, 100)  # Adjust based on your data scale
ax3.set_title('FFT Magnitude Spectrum')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Magnitude')

# Animation update function
def update_plot(frame):
    line.set_ydata(waveform_data[:frame+1])
    fft_line.set_ydata(fft_magnitude_data[:, frame])
    im.set_data(spectrogram_data[:, :frame+1])
    return im, line, fft_line

# Create animation
ani = FuncAnimation(fig, update_plot, frames=range(total_frames), blit=True, interval=1000 * hop_length / sampling_rate)

# Function to start audio playback
def audio_playback(audio, sampling_rate):
    sd.play(audio, samplerate=sampling_rate)
    sd.wait()

# Start audio playback in a separate thread to avoid blocking
playback_thread = threading.Thread(target=audio_playback, args=(audio, sampling_rate))
playback_thread.start()

plt.show()
