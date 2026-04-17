import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.io import wavfile
import subprocess
import sys
import os

# =========================
# CONFIG
# =========================
AUDIO_FILE = "no/1.wav"
TEMP_VIDEO = "temp_video.mp4"
FINAL_VIDEO = "final_output.mp4"

FPS = 60
FIGSIZE = (12, 4)
DPI = 200

# =========================
# LOAD AUDIO
# =========================
fs, data = wavfile.read(AUDIO_FILE)

# Normalize
if data.dtype != np.float32:
    data = data / np.max(np.abs(data))

# Convert to mono if needed
if len(data.shape) > 1:
    data = data.mean(axis=1)

t = np.arange(len(data)) / fs
duration = len(data) / fs

# =========================
# PLOT SETUP
# =========================
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

line, = ax.plot(
    t,
    data,
    lw=1.5,
    antialiased=True,
)

cursor = ax.axvline(
    0,
    linewidth=2.5,
)

ax.set_xlim(0, duration)
ax.set_ylim(-1.05, 1.05)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Amplitude")
ax.set_title("Waveform with Synchronized Cursor")
ax.grid(True, linestyle="--", alpha=0.4)

# =========================
# ANIMATION
# =========================
samples_per_frame = int(fs / FPS)
total_frames = int(np.ceil(len(data) / samples_per_frame))

def update(frame):
    current_sample = frame * samples_per_frame
    current_time = current_sample / fs
    cursor.set_xdata(current_time)
    return (cursor,)

ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    interval=1000 / FPS,
    blit=True
)

# =========================
# SAVE TEMP VIDEO (NO AUDIO)
# =========================
writer = FFMpegWriter(fps=FPS, bitrate=3200)

print("Rendering video...")
ani.save(TEMP_VIDEO, writer=writer)
print("Video rendering done.")

# =========================
# MERGE AUDIO USING FFMPEG
# =========================
ffmpeg_cmd = [
    "ffmpeg",
    "-y",  # overwrite
    "-i", TEMP_VIDEO,
    "-i", AUDIO_FILE,
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    FINAL_VIDEO
]

print("Merging audio with FFmpeg...")

try:
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Final video saved as: {FINAL_VIDEO}")

    # Optional: remove temp file
    os.remove(TEMP_VIDEO)

except subprocess.CalledProcessError:
    print("FFmpeg failed. Make sure ffmpeg is installed and in PATH.")
    sys.exit(1)
  
