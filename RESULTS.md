\# Simulation Results, Graphs, and Formulas  

\### Double‑Slit Information‑Compression Model



This document defines the main measurable quantities in the simulation and how

they relate to the information‑compression model. It also describes how to

extract them from numerical runs and plot them as graphs.



\---



\## 1. Core state variables



The model uses a continuous information‑state (compression) parameter:



\- \\( c \\in \[0, 1] \\)

\- \\( c = 0 \\): fully decompressed (pure wave)

\- \\( c = 1 \\): fully compressed (pure particle)



The wavefunction on the screen is \\( \\psi(x) \\), and the intensity is:







\\\[

I(x) = |\\psi(x)|^2

\\]







All observable patterns (interference, collapse, packet shape) are derived from

\\( I(x) \\) under different values and histories of \\( c \\).



\---



\## 2. Interference visibility \\( V(c) \\)



For a given compression level \\( c \\), the interference visibility is defined as:







\\\[

V(c) = \\frac{I\_{\\max}(c) - I\_{\\min}(c)}{I\_{\\max}(c) + I\_{\\min}(c)}

\\]







where:



\- \\( I\_{\\max}(c) \\) = average peak intensity of bright fringes  

\- \\( I\_{\\min}(c) \\) = average intensity of dark fringes between peaks  



\*\*Simulation procedure:\*\*



1\. Fix a compression strength \\( c \\) (e.g. `partial\_info\_strength = c`).

2\. Run the double‑slit simulation to the screen.

3\. Sample \\( I(x) \\) along the detection line.

4\. Find local maxima and minima to estimate \\( I\_{\\max}(c) \\) and \\( I\_{\\min}(c) \\).

5\. Compute \\( V(c) \\) using the formula above.

6\. Repeat for \\( c \\in \[0, 1] \\) and plot \\( V(c) \\).



\*\*Model expectation (example functional form):\*\*







\\\[

V(c) \\approx 1 - c

\\]







This gives a simple, testable prediction: visibility decreases smoothly with

compression strength.



\---



\## 3. Distinguishability \\( D(c) \\) and complementarity



Define a path‑distinguishability \\( D(c) \\) proportional to compression:







\\\[

D(c) \\approx c

\\]







Then the model provides a natural mapping between visibility and

distinguishability:







\\\[

V(c) \\approx 1 - c, \\quad D(c) \\approx c

\\]







so that:







\\\[

V^2(c) + D^2(c) = (1 - c)^2 + c^2

\\]







This relation can be compared directly with experimental data on partial

which‑path detection and weak measurements.



\---



\## 4. Collapsed packet shape and detector geometry



When a detector fires, the model applies a localized compression kernel

centered at position \\( x\_0 \\):







\\\[

\\psi\_{\\text{collapsed}}(x) \\propto \\psi(x) \\cdot K(x - x\_0)

\\]







For a Gaussian kernel:







\\\[

K(x - x\_0) = \\exp\\left( -\\frac{(x - x\_0)^2}{2\\sigma^2} \\right)

\\]







\*\*Prediction:\*\*



\- The spatial profile of the collapsed packet on the screen reflects the

&#x20; detector kernel \\( K \\).

\- Changing detector size/shape (i.e. \\( \\sigma \\) or kernel form) changes the

&#x20; observed packet shape.



\*\*Simulation procedure:\*\*



1\. Implement different detector kernels \\( K \\) (narrow, wide, non‑Gaussian).

2\. Trigger collapse at the slits.

3\. Propagate to the screen and record \\( I\_{\\text{collapsed}}(x) \\).

4\. Compare packet shapes for different kernels.



\---



\## 5. Hysteresis: history‑dependent behavior



The model allows sequences of compression and re‑decompression:



\- Protocol A: direct compression to \\( c = c\_f \\)

\- Protocol B: compress to \\( c = 1 \\), decompress to \\( c = 0 \\), then to \\( c\_f \\)



Let \\( V\_A(c\_f) \\) and \\( V\_B(c\_f) \\) be the final visibilities for the two

protocols.



\*\*Prediction (if hysteresis is present):\*\*







\\\[

V\_A(c\_f) \\neq V\_B(c\_f)

\\]







even though the final compression level \\( c\_f \\) is the same.



\*\*Simulation procedure:\*\*



1\. Implement different compression histories with the same final \\( c\_f \\).

2\. Run to the screen and compute \\( V \\) for each protocol.

3\. Plot \\( V \\) vs \\( c\_f \\) for different histories on the same graph.



\---



\## 6. Timing of re‑decompression



Let \\( t\_d \\) be the delay between compression and re‑decompression.



Define \\( V(c, t\_d) \\) as the visibility after:



\- compressing to \\( c \\)

\- holding that state for time \\( t\_d \\)

\- re‑decompressing

\- propagating to the screen



\*\*Prediction (example qualitative form):\*\*







\\\[

V(c, t\_d) \\le V(c, 0)

\\]







with possible gradual reduction of maximum recoverable visibility as \\( t\_d \\)

increases.



\*\*Simulation procedure:\*\*



1\. Compress at time \\( t = t\_0 \\).

2\. Hold the compressed state for different durations \\( t\_d \\).

3\. Re‑decompress and propagate to the screen.

4\. Compute \\( V(c, t\_d) \\) and plot visibility vs delay.



\---



\## 7. How to generate graphs from the engine



In practice:



\- Use the engine to output \\( I(x) \\) arrays for different:

&#x20; - compression strengths \\( c \\)

&#x20; - histories

&#x20; - detector kernels

&#x20; - timing delays

\- Compute:

&#x20; - \\( V(c) \\)

&#x20; - \\( D(c) \\)

&#x20; - packet profiles

\- Plot:

&#x20; - \\( V(c) \\) vs \\( c \\)

&#x20; - \\( V^2(c) + D^2(c) \\) vs \\( c \\)

&#x20; - packet shapes for different kernels

&#x20; - \\( V(c, t\_d) \\) vs \\( t\_d \\)



These graphs turn the qualitative behavior of the simulation into quantitative,

testable relationships.



\---



