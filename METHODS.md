\# Methods  

\### Simulation and Quantitative Extraction Procedures  

Double‑Slit Information‑Compression Model  

Author: Thomas Price (2026)



This section describes how numerical results were generated from the

Information‑Compression Engine and how key physical quantities were extracted

from the simulated wavefunction data.



\---



\## 1. Simulation Framework



All simulations were performed using the custom Python engine included in this

repository. The engine evolves a 2D complex wavefunction ψ(x, y) using a

discrete propagation step and applies information‑state transitions through a

compression parameter:



&#x20;   c ∈ \[0, 1]



where:

\- c = 0 → fully decompressed (wave-like)

\- c = 1 → fully compressed (particle-like)



The engine supports:

\- free propagation

\- slit masks

\- detector-triggered compression

\- re-decompression

\- partial-information states

\- directional Gaussian packet formation



The real part Re(ψ) and intensity I(x) = |ψ|² are sampled at the detection

screen for all analyses.



\---



\## 2. Extraction of Interference Visibility V(c)



For each compression level c, the intensity profile I(x) along the detection

screen is computed by summing |ψ(x, y)|² over the vertical axis.



Local maxima and minima are identified using a simple peak-finding routine.

Visibility is computed as:



&#x20;   V(c) = (I\_max(c) − I\_min(c)) / (I\_max(c) + I\_min(c))



Procedure:

1\. Run simulation with fixed compression c.

2\. Extract 1D intensity profile I(x).

3\. Identify fringe peaks and troughs.

4\. Compute V(c).

5\. Repeat for c ∈ \[0, 1] in increments (e.g., 0.05).



This produces the visibility curve V(c).



\---



\## 3. Distinguishability D(c)



Path distinguishability is defined directly from the compression parameter:



&#x20;   D(c) = c



This reflects the model’s interpretation of compression as information gain

about the particle’s path.



The complementarity relation is evaluated as:



&#x20;   V²(c) + D²(c)



and compared to the simulation-derived V(c).



\---



\## 4. Collapse Kernel and Packet Shape



When a detector triggers, the wavefunction is multiplied by a localized kernel

centered at the detection coordinate x₀:



&#x20;   ψ\_collapsed(x) = ψ(x) · K(x − x₀)



The default kernel is Gaussian:



&#x20;   K(x − x₀) = exp(−(x − x₀)² / (2σ²))



To analyze packet shape:

1\. Trigger collapse at the slit plane.

2\. Propagate ψ to the detection screen.

3\. Extract I(x) = |ψ(x)|².

4\. Fit the resulting packet to the kernel form to verify shape retention.



Different detector geometries are tested by modifying K.



\---



\## 5. Hysteresis Protocols



To test history dependence, multiple compression sequences are applied:



\- Protocol A: direct compression to c\_f  

\- Protocol B: compress → decompress → recompress to c\_f  



For each protocol:

1\. Apply the compression sequence.

2\. Propagate to the screen.

3\. Compute V(c\_f) as described above.



Differences between V\_A(c\_f) and V\_B(c\_f) indicate hysteresis.



\---



\## 6. Timing-Dependent Re-Decompression



To evaluate timing effects:

1\. Compress the wavefunction at time t₀.

2\. Hold the compressed state for delay t\_d.

3\. Re-decompress to c = 0.

4\. Propagate to the screen.

5\. Compute V(c, t\_d).



Visibility is plotted as a function of delay t\_d.



\---



\## 7. Numerical Implementation Details



\- Spatial grid: 2D uniform grid (resolution defined in engine config)

\- Time stepping: fixed Δt propagation

\- Boundary conditions: absorbing edges

\- Slit mask: binary aperture applied at propagation step

\- Detector model: probabilistic trigger based on local intensity

\- Compression strength: linear scaling of kernel amplitude



All simulations are reproducible using the included Python scripts.



\---



