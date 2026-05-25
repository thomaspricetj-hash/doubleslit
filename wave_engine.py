import numpy as np


class WaveField2D:
    """
    2D information-physics wave engine with:

    - Schrödinger-like propagation (wave / decompressed info)
    - Localized Gaussian compression (particle / compressed info)
    - Directional particle propagation
    - Partial-information states (0..1, not just 0/1)
    - Multi-detector support (left/right)
    - Probability-based collapse
    - Global information controller hooks
    - Explicit state map:
        state[y, x] in [0, 1]
        0.0 = pure wave (fully decompressed)
        1.0 = pure particle (fully compressed)
    """

    def __init__(self, nx, ny, dx=1.0, dy=1.0, dt=0.01, c=1.0):
        self.nx = nx
        self.ny = ny
        self.dx = dx
        self.dy = dy
        self.dt = dt
        self.c = c

        # complex wave field
        self.psi = np.zeros((ny, nx), dtype=np.complex128)

        # barrier mask (1 = wall, 0 = free)
        self.barrier = np.zeros((ny, nx), dtype=np.float64)

        # multi-detector masks
        self.detector_left = np.zeros((ny, nx), dtype=np.float64)
        self.detector_right = np.zeros((ny, nx), dtype=np.float64)

        # state map: 0..1 (0 = wave, 1 = particle)
        self.state = np.zeros((ny, nx), dtype=np.float32)

        # global information / collapse controls
        self.detectors_enabled = True
        self.collapse_probability = 1.0       # 0..1
        self.partial_info_strength = 1.0      # 0..1 (how strong compression is)

        # single "particle packet" tracking for directional propagation
        self.particle_center = None           # (cx, cy) in float coords
        self.particle_direction = np.array([1.0, 0.0], dtype=np.float64)  # default: to the right
        self.particle_radius = 8.0
        self.particle_speed = 1.0             # cells per step

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    def set_barrier(self, mask):
        self.barrier = mask.astype(np.float64)

    def set_detectors(self, left_mask, right_mask):
        self.detector_left = left_mask.astype(np.float64)
        self.detector_right = right_mask.astype(np.float64)

    def set_info_config(self, detectors_enabled=None,
                        collapse_probability=None,
                        partial_info_strength=None,
                        particle_speed=None):
        if detectors_enabled is not None:
            self.detectors_enabled = detectors_enabled
        if collapse_probability is not None:
            self.collapse_probability = float(collapse_probability)
        if partial_info_strength is not None:
            self.partial_info_strength = float(partial_info_strength)
        if particle_speed is not None:
            self.particle_speed = float(particle_speed)

    # ------------------------------------------------------------------
    # Core wave evolution
    # ------------------------------------------------------------------
    def add_source(self, x, y, amplitude=0.05):
        if 0 <= x < self.nx and 0 <= y < self.ny:
            self.psi[y, x] += amplitude

    def laplacian(self, field):
        lap = np.zeros_like(field)
        lap[1:-1, 1:-1] = (
            field[1:-1, 0:-2] +
            field[1:-1, 2:] +
            field[0:-2, 1:-1] +
            field[2:, 1:-1] -
            4.0 * field[1:-1, 1:-1]
        )
        return lap

    def step(self):
        """
        Wave evolution step:
        - regions with low compression (state ~ 0) evolve as wave
        - highly compressed regions (state ~ 1) are mostly frozen and
          handled by directional particle propagation
        """
        lap = self.laplacian(self.psi)

        # evolve only where state < 0.99 (wave / partially compressed)
        wave_mask = (self.state < 0.99)
        self.psi[wave_mask] += 1j * self.c * self.dt * lap[wave_mask]

        # zero out inside barrier
        self.psi[self.barrier > 0.5] = 0.0

        # update particle packet if present
        self._update_particle_packet()

    def intensity(self):
        return np.abs(self.psi) ** 2

    # ------------------------------------------------------------------
    # Compression / decompression primitives
    # ------------------------------------------------------------------
    def _gaussian_mask(self, center, radius):
        cx, cy = center
        yy, xx = np.mgrid[0:self.ny, 0:self.nx]
        dist2 = (xx - cx) ** 2 + (yy - cy) ** 2
        mask = dist2 < radius ** 2
        gaussian = np.exp(-dist2[mask] / (2 * (radius / 2) ** 2))
        return mask, gaussian

    def compress_region_gaussian(self, center, radius=6.0, strength=1.0):
        """
        Compress information locally into a Gaussian packet (particle mode).
        - center: (cx, cy) in float coords
        - radius: spatial extent of packet
        - strength: 0..1, how strongly we compress (partial info)
        """
        strength = np.clip(strength, 0.0, 1.0)
        mask, gaussian = self._gaussian_mask(center, radius)

        if not np.any(mask):
            return

        # update state: move toward 1.0 by 'strength'
        self.state[mask] = np.clip(self.state[mask] + strength * (1.0 - self.state[mask]), 0.0, 1.0)

        # remove imaginary part in compressed region
        self.psi[mask] = np.real(self.psi[mask])

        # blend existing amplitude with Gaussian packet
        # strength controls how much we overwrite
        self.psi[mask] = (1.0 - strength) * self.psi[mask] + strength * gaussian

        # track particle packet center and radius for directional propagation
        self.particle_center = np.array(center, dtype=np.float64)
        self.particle_radius = float(radius)

    def decompress_region(self, mask=None):
        """
        Re-decompress compressed regions back into wave mode.
        - mask: boolean mask; if None, decompress all cells with state > 0.
        We keep ψ as-is but reintroduce a small random phase so it can
        spread and interfere again under evolution.
        """
        if mask is None:
            mask = (self.state > 0.0)

        if not np.any(mask):
            return

        # mark back toward wave mode
        self.state[mask] = 0.0

        # reintroduce a small random phase
        phase = np.random.uniform(-0.3, 0.3, size=np.count_nonzero(mask))
        self.psi[mask] = self.psi[mask] * np.exp(1j * phase)

        # if everything is decompressed, drop particle tracking
        if not np.any(self.state > 0.9):
            self.particle_center = None

    # ------------------------------------------------------------------
    # Directional particle propagation
    # ------------------------------------------------------------------
    def _update_particle_packet(self):
        """
        If a particle packet is being tracked, move its center along
        self.particle_direction and rebuild the Gaussian packet there.
        """
        if self.particle_center is None:
            return

        # move center
        self.particle_center += self.particle_direction * self.particle_speed

        cx, cy = self.particle_center
        if cx < 0 or cx >= self.nx or cy < 0 or cy >= self.ny:
            # packet left the domain
            self.particle_center = None
            return

        # rebuild Gaussian at new center, only in highly compressed region
        mask, gaussian = self._gaussian_mask(self.particle_center, self.particle_radius)
        if not np.any(mask):
            return

        # keep state near 1 in this region
        self.state[mask] = np.clip(self.state[mask] + 0.2 * (1.0 - self.state[mask]), 0.0, 1.0)

        # overwrite ψ in that region with the moving packet
        self.psi[mask] = gaussian

    # ------------------------------------------------------------------
    # Detector-driven compression (wave -> particle)
    # ------------------------------------------------------------------
    def apply_detectors(self, threshold=0.02, rng=None):
        """
        If intensity in a detector region exceeds threshold:
        - with probability collapse_probability:
            - compute hit centroid
            - compress that region into a Gaussian packet
            - mark it as particle mode in the state map
        Returns:
            event_info dict or None
        """
        if not self.detectors_enabled:
            return None

        if rng is None:
            rng = np.random

        intensity = np.abs(self.psi) ** 2

        events = []

        for name, det_mask in (("left", self.detector_left), ("right", self.detector_right)):
            hit_mask = (det_mask > 0.5) & (intensity > threshold)
            if np.any(hit_mask):
                if rng.random() <= self.collapse_probability:

                    ys, xs = np.where(hit_mask)
                    cx = float(np.mean(xs))
                    cy = float(np.mean(ys))

                    # direction: from slit toward screen (to the right)
                    self.particle_direction = np.array([1.0, 0.0], dtype=np.float64)

                    self.compress_region_gaussian(
                        center=(cx, cy),
                        radius=8.0,
                        strength=self.partial_info_strength
                    )

                    events.append({"detector": name, "center": (cx, cy)})

        if not events:
            return None

        # if multiple detectors fired, just return list
        return {"type": "collapse", "events": events}

    # ------------------------------------------------------------------
    # Video-game-style LOD
    # ------------------------------------------------------------------
    def apply_lod(self, distance_map, lod_threshold=80):
        """
        Minimal render far away (still in wave mode).
        Particle regions (state ~ 1) are left alone.
        """
        far_mask = (distance_map > lod_threshold) & (self.state < 0.99)

        self.psi[far_mask] *= 0.1
        self.psi[far_mask] = np.exp(1j * np.angle(self.psi[far_mask]))





