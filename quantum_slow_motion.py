import os
import shutil
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# -----------------------------
# CONFIG
# -----------------------------
FPS = 24
DURATION = 40.0  # seconds
N_FRAMES = int(FPS * DURATION)

WIDTH = 1280
HEIGHT = 720

BACKGROUND_COLOR = (0, 0, 0)
WAVE_COLOR = np.array([0.0, 0.9, 0.9])  # soft teal
PARTICLE_COLOR = np.array([1.0, 1.0, 1.0])

# particle path (normalized coordinates)
X_START = -0.8
X_END = 0.8
Y_POS = 0.0

# sigma values
SIGMA_PARTICLE = 0.03
SIGMA_WAVE = 0.22

# detector x position (normalized)
DETECTOR_X = 0.65
DETECTOR_WIDTH = 0.08
DETECTOR_HEIGHT = 0.6

# caption fade config
CAPTION_FADE = 0.7  # seconds
CAPTION_OVERLAP = 0.5  # seconds

# -----------------------------
# CAPTION SCHEDULE (seconds)
# -----------------------------
captions = [
    (0.0, 6.0, "A single particle is emitted from the laser."),
    (5.5, 11.5, "The particle travels forward, still compressed."),
    (11.0, 18.5, "Without observation, the particle decompresses into a wave."),
    (18.0, 22.5, "A detector begins observing the wave."),
    (22.0, 25.5, "Observation collapses the wave into a particle."),
    (25.0, 29.5, "Observation ends."),
    (29.0, 36.0, "Without observation, the particle decompresses back into a wave."),
    (35.5, 40.0, "The wave evolves freely through space."),
]

# -----------------------------
# SIGMA / STATE SCHEDULE
# -----------------------------
# We define time regions (seconds) for behavior:
# 0–8s: compressed particle
# 8–16s: decompression to wave
# 16–20s: detector observing (collapse)
# 20–30s: decompression again
# 30–40s: free wave

def sigma_for_time(t):
    if t < 8.0:
        return SIGMA_PARTICLE
    elif t < 16.0:
        # linear from particle to wave
        alpha = (t - 8.0) / (16.0 - 8.0)
        return (1 - alpha) * SIGMA_PARTICLE + alpha * SIGMA_WAVE
    elif t < 20.0:
        return SIGMA_PARTICLE
    elif t < 30.0:
        alpha = (t - 20.0) / (30.0 - 20.0)
        return (1 - alpha) * SIGMA_PARTICLE + alpha * SIGMA_WAVE
    else:
        return SIGMA_WAVE

def detector_active(t):
    return 16.0 <= t <= 20.0

def is_wave_state(t):
    # used only for visual emphasis (slightly stronger glow when wave-like)
    return (8.0 <= t < 16.0) or (20.0 <= t <= 40.0)

# -----------------------------
# CAPTION ALPHA
# -----------------------------
def caption_alpha(t, start, end):
    if t < start or t > end:
        return 0.0
    # fade in
    if start <= t < start + CAPTION_FADE:
        return (t - start) / CAPTION_FADE
    # fade out
    if end - CAPTION_FADE < t <= end:
        return (end - t) / CAPTION_FADE
    return 1.0

# -----------------------------
# MAIN RENDER LOOP
# -----------------------------
def main():
    # prepare grid in normalized coordinates
    x = np.linspace(-1.0, 1.0, WIDTH)
    y = np.linspace(-0.5, 0.5, HEIGHT)  # narrower vertically
    X, Y = np.meshgrid(x, y)

    os.makedirs("frames_quantum", exist_ok=True)

    for frame in range(N_FRAMES):
        t = frame / FPS  # seconds

        # particle center position
        frac = frame / max(N_FRAMES - 1, 1)
        x_c = X_START + (X_END - X_START) * frac
        y_c = Y_POS

        sigma = sigma_for_time(t)

        # Gaussian field
        r2 = (X - x_c) ** 2 + (Y - y_c) ** 2
        field = np.exp(-r2 / (2.0 * sigma * sigma))

        # emphasize wave vs particle visually
        if is_wave_state(t):
            intensity = field
        else:
            intensity = field ** 1.5  # slightly sharper for particle

        intensity /= intensity.max() + 1e-12

        # map to RGB
        img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
        # background
        img[:, :, :] = BACKGROUND_COLOR

        # wave color
        wave_layer = intensity[..., None] * WAVE_COLOR[None, None, :]
        img += wave_layer

        # clamp
        img = np.clip(img, 0.0, 1.0)

        # detector visualization
        fig, ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100)
        ax.imshow(img, origin="lower", extent=[-1, 1, -0.5, 0.5])

        # draw detector on the right
        det_color = (0.3, 0.3, 0.3)
        if detector_active(t):
            det_color = (0.9, 0.2, 0.2)
        det_rect = Rectangle(
            (DETECTOR_X, -DETECTOR_HEIGHT / 2),
            DETECTOR_WIDTH,
            DETECTOR_HEIGHT,
            linewidth=1.5,
            edgecolor="white",
            facecolor=det_color,
            alpha=0.9,
        )
        ax.add_patch(det_rect)

        # draw laser source on the left
        laser_rect = Rectangle(
            (X_START - 0.05, -0.15),
            0.05,
            0.3,
            linewidth=1.5,
            edgecolor="white",
            facecolor=(0.2, 0.2, 0.8),
            alpha=0.9,
        )
        ax.add_patch(laser_rect)

        # beam line
        ax.plot([X_START - 0.05, x_c], [0.0, 0.0], color=(0.7, 0.7, 1.0), linewidth=1.0, alpha=0.6)

        # captions (centered, medium, white with soft shadow)
        active_texts = []
        for (start, end, text) in captions:
            alpha = caption_alpha(t, start, end)
            if alpha > 0.01:
                active_texts.append((text, alpha))

        for text, alpha in active_texts:
            # shadow
            ax.text(
                0.0,
                -0.38,
                text,
                ha="center",
                va="center",
                fontsize=20,
                color="black",
                alpha=alpha * 0.6,
                transform=ax.transData,
            )
            # main text
            ax.text(
                0.0,
                -0.38,
                text,
                ha="center",
                va="center",
                fontsize=20,
                color="white",
                alpha=alpha,
                transform=ax.transData,
            )

        ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        out_name = os.path.join("frames_quantum", f"quantum_{frame:04d}.png")
        plt.savefig(out_name, dpi=100)
        plt.close(fig)

        print(f"[{frame+1}/{N_FRAMES}] saved {out_name}")

    # build video with ffmpeg
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        print("ffmpeg not found in PATH – skipping video build.")
        print("Frames are in ./frames_quantum/")
        return

    cmd = [
        ffmpeg_path,
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        os.path.join("frames_quantum", "quantum_%04d.png"),
        "-pix_fmt",
        "yuv420p",
        "quantum_slow_motion.mp4",
    ]
    print("Running ffmpeg to build quantum_slow_motion.mp4 ...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("quantum_slow_motion.mp4 created successfully. Cleaning up PNG frames...")
        for fname in os.listdir("frames_quantum"):
            if fname.endswith(".png"):
                os.remove(os.path.join("frames_quantum", fname))
        os.rmdir("frames_quantum")
        print("Cleanup done.")
    else:
        print("ffmpeg failed, keeping PNG frames for debugging.")
        print(result.stderr)


if __name__ == "__main__":
    main()
