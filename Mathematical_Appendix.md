MATHEMATICAL APPENDIX

Information‑Compression Model (ICM)

Author: Thomas Price

Year: 2026

============================================================

This appendix defines the mathematical structures used in the Information‑Compression Model.

All notation is ASCII‑safe and compatible with plain‑text editors.



The goal is to provide a clear, formal description of:



State representation



Compression and decompression operators



Collapse kernels



Evolution rules



Visibility and distinguishability mappings



Multi‑pass compression behavior



Detector‑geometry effects



This appendix supports the predictions, postulates, and experiments defined elsewhere in the repository.



STATE REPRESENTATION



A quantum state is represented as:



psi(x)



This is the decompressed (wave‑like) form.



A compressed (particle‑like) state is represented as:



psi\_c(x)



Compression is controlled by a scalar:



c in \[0, 1]



Where:

c = 0  -> fully wave‑like

c = 1  -> fully particle‑like



COMPRESSION OPERATOR



Compression is implemented by multiplying the state by a kernel K:



psi\_c(x) = psi(x) \* K(x)



Where K(x) is a localized function centered on the detection region.



General form:



K(x) = exp( - (x - x0)^2 / (2 \* sigma^2) )



Parameters:

x0    = center of collapse

sigma = kernel width (controls collapse strength)



Interpretation:

Small sigma  -> strong collapse

Large sigma  -> weak collapse



DECOMPRESSION OPERATOR (INVERSE COLLAPSE)



Decompression is the inverse operation:



psi(x) = psi\_c(x) / K(x)



This is well‑defined as long as K(x) is nonzero everywhere.



Interpretation:

Erasure = dividing out the collapse kernel.



PARTIAL COMPRESSION



Partial collapse is represented by raising the kernel to a power c:



psi\_c(x) = psi(x) \* K(x)^c



Where:

c = compression strength (0 to 1)



Special cases:

c = 0  -> psi\_c(x) = psi(x)

c = 1  -> full collapse

0 < c < 1  -> partial collapse



MULTI‑PASS COMPRESSION



Sequential compressions compound multiplicatively:



psi\_c(x) = psi(x) \* K1(x)^c1 \* K2(x)^c2 \* K3(x)^c3 ...



If all kernels are identical:



psi\_c(x) = psi(x) \* K(x)^(c1 + c2 + c3 + ...)



ICM prediction:

The effective compression is NOT linear due to hysteresis and kernel overlap.



VISIBILITY MAPPING



Interference visibility V is defined as:



V = (I\_max - I\_min) / (I\_max + I\_min)



ICM prediction:

V = 1 - c



Standard QM prediction:

V depends on coherence, not a compression parameter.



DISTINGUISHABILITY MAPPING



Distinguishability D is defined as:



D = c



ICM complementarity rule:



D + V = 1



Standard QM rule:



D^2 + V^2 <= 1



COLLAPSE SHAPE AND DETECTOR GEOMETRY



The collapse kernel K(x) inherits the geometry of the detector.



Examples:



Rectangular detector:

K(x) = 1 inside region, 0 outside



Circular detector:

K(x) = exp( - r^2 / (2 \* sigma^2) )



Asymmetric detector:

K(x) = exp( - (x - x0)^2 / (2 \* sigma\_left^2) ) for x < x0

K(x) = exp( - (x - x0)^2 / (2 \* sigma\_right^2) ) for x > x0



ICM prediction:

Collapse shape mirrors detector geometry.



TIME‑DEPENDENT COMPRESSION



If compression persists for time t before erasure:



psi\_recovered(x) = psi(x) \* K(x)^c \* F(t)



Where F(t) is a recovery factor:



F(t) decreases slowly with time



ICM prediction:

Longer compression -> less recoverable interference.



Standard QM prediction:

Recovery is time‑independent.



HIDDEN STRUCTURE IN PARTIAL COLLAPSE



Partial collapse preserves sub‑interference structure:



psi\_c(x) = psi(x) \* K(x)^c



Hidden structure can be recovered by:



psi\_recovered(x) = psi\_c(x) / K(x)^c



ICM prediction:

Partial collapse is reversible.



Standard QM prediction:

Lost coherence is irrecoverable.



INFORMATION FLOW EQUATIONS



Information content I is split into:



I\_wave  = (1 - c)

I\_part  = c



Total information is conserved:



I\_total = I\_wave + I\_part = 1



Measurement:

c increases



Erasure:

c decreases



SUMMARY OF MATHEMATICAL STRUCTURE



The Information‑Compression Model is defined by:



psi(x)               = decompressed state



psi\_c(x)             = compressed state



K(x)                 = collapse kernel



psi\_c = psi \* K^c    = compression



psi = psi\_c / K^c    = decompression



V = 1 - c            = visibility



D = c                = distinguishability



D + V = 1            = complementarity



sigma                = collapse strength parameter



Detector geometry   = determines K(x)



Multi‑pass collapse = non‑linear



Information is conserved



This appendix provides the formal mathematical foundation for the entire theory.



============================================================

