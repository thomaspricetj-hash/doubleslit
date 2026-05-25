import numpy as np
import matplotlib.pyplot as plt
from wave_engine import WaveField2D


def make_double_slit_mask(nx, ny, slit_y_center, slit_sep, slit_height, barrier_x):
    mask = np.zeros((ny, nx), dtype=np.float64)
    mask[:, barrier_x] = 1.0

    half_h = slit_height // 2

    slit1_center = slit_y_center - slit_sep // 2
    slit2_center = slit_y_center + slit_sep // 2

    y1_start = slit1_center - half_h
    y1_end   = slit1_center + half_h

    y2_start = slit2_center - half_h
    y2_end   = slit2_center + half_h

    mask[y1_start:y1_end, barrier_x] = 0.0
    mask[y2_start:y2_end, barrier_x] = 0.0

    return mask


def make_detector_masks(nx, ny, barrier_x, slit_y_center, slit_sep, slit_height):
    left = np.zeros((ny, nx), dtype=np.float64)
    right = np.zeros((ny, nx), dtype=np.float64)

    half_h = slit_height // 2

    slit1_center = slit_y_center - slit_sep // 2
    slit2_center = slit_y_center + slit_sep // 2

    y1_start = slit1_center - half_h
    y1_end   = slit1_center + half_h

    y2_start = slit2_center - half_h
    y2_end   = slit2_center + half_h

    # left slit detector just behind barrier
    left[y1_start:y1_end, barrier_x + 1] = 1.0
    # right slit detector just behind barrier
    right[y2_start:y2_end, barrier_x + 1] = 1.0

    return left, right


def main():
    nx, ny = 400, 200
    field = WaveField2D(nx, ny, dt=0.02, c=0.5)

    barrier_x = nx // 2
    slit_y_center = ny // 2
    slit_sep = 40
    slit_height = 20

    barrier = make_double_slit_mask(nx, ny, slit_y_center, slit_sep, slit_height, barrier_x)
    field.set_barrier(barrier)

    det_left, det_right = make_detector_masks(nx, ny, barrier_x, slit_y_center, slit_sep, slit_height)
    field.set_detectors(det_left, det_right)

    # global info config
    field.set_info_config(
        detectors_enabled=True,
        collapse_probability=0.9,      # high but not absolute
        partial_info_strength=0.9,     # strong compression
        particle_speed=1.0
    )

    source_x = nx // 8
    source_y = ny // 2

    yy, xx = np.mgrid[0:ny, 0:nx]
    distance_map = np.sqrt((xx - source_x) ** 2 + (yy - source_y) ** 2)

    # experiment timing
    total_steps = 2000
    decompress_time = 1300  # after this, info is "removed" → re-decompression

    # capture stages
    capture_times = [150, 450, 900, 1700]
    snapshots = []
    state_snapshots = []
    event_log = []

    rng = np.random.default_rng(1234)

    for t in range(total_steps):
        field.add_source(source_x, source_y, amplitude=0.05)
        field.step()

        field.apply_lod(distance_map, lod_threshold=80)

        # before decompress_time: detectors active → compression possible
        if t < decompress_time:
            event = field.apply_detectors(threshold=0.02, rng=rng)
            if event is not None:
                event["step"] = t
                event_log.append(event)
                print(f"[step {t}] collapse event: {event}")
        else:
            # after decompress_time: simulate info removal → re-decompression
            if field.detectors_enabled:
                print(f"[step {t}] turning detectors OFF and re-decompressing")
                field.set_info_config(detectors_enabled=False)
            field.decompress_region()

        if t in capture_times:
            snapshots.append(np.real(field.psi).copy())
            state_snapshots.append(field.state.copy())
            print(f"[step {t}] captured snapshot")

    # ---------------------------------------------------------
    # Plot: overlaid wave snapshots + final state overlay + particle center
    # ---------------------------------------------------------
    plt.figure(figsize=(12, 5))

    # base: wave snapshots overlaid
    alphas = [0.25, 0.35, 0.45, 0.55]
    for snap, a in zip(snapshots, alphas):
        plt.imshow(
            snap,
            cmap="coolwarm",
            origin="lower",
            aspect="auto",
            alpha=a
        )

    # overlay: last state map (compressed regions)
    if state_snapshots:
        state_last = state_snapshots[-1]
        plt.imshow(
            state_last,
            cmap="Greens",
            origin="lower",
            aspect="auto",
            alpha=0.35,
            vmin=0.0,
            vmax=1.0
        )

    # mark particle center if still present
    if field.particle_center is not None:
        cx, cy = field.particle_center
        plt.scatter([cx], [cy], c="yellow", s=40, marker="x", label="particle center")

    plt.title("Wave ↔ Particle via Compression / Re-Decompression\n"
              "(State Map, Directional Packet, Probabilistic Collapse)")
    plt.colorbar(label="Re(ψ)")
    plt.tight_layout()
    plt.savefig("double_slit_full_info_physics_engine.png")
    plt.close()

    print("Saved: double_slit_full_info_physics_engine.png")
    print("Event log:")
    for e in event_log:
        print(e)


if __name__ == "__main__":
    main()








