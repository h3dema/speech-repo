import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

def analyze_audio(file_path, save_path: str | None = None):
    # 1. Read the wav file
    # sample_rate is samples per second (Hz)
    # data is the actual audio amplitude
    sample_rate, data = wavfile.read(file_path)

    # If the audio is stereo (2 channels), convert to mono by averaging
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Calculate time axis for the amplitude plot
    duration = len(data) / sample_rate
    print(f"Sample Rate: {sample_rate} Hz, Duration: {duration:.2f} seconds")
    time = np.linspace(0., duration, len(data))

    # 2. Create the plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8)) # , sharex=True)
    plt.subplots_adjust(hspace=0.4)

    # --- Plot Amplitude vs Time ---
    ax1.plot(time, data, color='teal', linewidth=0.5)
    ax1.set_title('Amplitude vs Time (Waveform)')
    ax1.set_ylabel('Amplitude')
    ax1.set_xlabel('Time [sec]')
    ax1.grid(True, alpha=0.3)

    # # Create an array of tick positions from 0 to duration
    # tick_interval = duration / 2
    # xtick_positions = np.arange(0, duration + tick_interval, tick_interval)
    # ax1.set_xticks(xtick_positions)

    # --- Compute and Plot Spectrogram ---
    # nperseg defines the length of each segment for the Fourier Transform
    frequencies, times, spectrogram = signal.spectrogram(data, sample_rate)

    # Use pcolormesh to plot the frequency intensities
    # cmap='magma' or 'viridis' are great for visibility
    im = ax2.pcolormesh(times, frequencies, 10 * np.log10(spectrogram),
                        shading='gouraud', cmap='magma')

    ax2.set_title('Spectrogram (Frequency vs Time)')
    ax2.set_ylabel('Frequency [Hz]')
    ax2.set_xlabel('Time [sec]')

    # Add a colorbar to show intensity levels
    fig.colorbar(im, ax=ax2, label='Intensity [dB]')

    if save_path:
        # Save the plot as an image()
        plt.savefig(save_path)
    else:
        plt.show()
    plt.close()


# Example usage:
# analyze_audio('your_audio_file.wav')