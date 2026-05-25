SIMULATION ENGINE DOCUMENTATION

Information‑Compression Model (ICM)

Double‑Slit Information‑Physics Engine

Author: Thomas Price

Year: 2026

============================================================

This document describes the architecture, behavior, and usage of the Simulation Engine used to model the Information‑Compression framework.

The engine implements reversible compression, decompression, collapse kernels, visibility calculations, and multi‑pass information flow.



It is designed to be:



deterministic



reproducible



modular



extensible



physically interpretable



The engine is not a toy model; it is a computational implementation of the core postulates of the ICM.



PURPOSE OF THE SIMULATION ENGINE



The engine provides a numerical environment for:



modeling wave‑to‑particle transitions



testing compression and decompression operations



simulating collapse kernels



generating interference patterns



validating predictions



exploring detector geometry effects



reproducing hysteresis and multi‑pass compression



It is the computational backbone of the theory.



STATE REPRESENTATION



The engine represents a quantum state as a 1D or 2D array:



psi\[x] or psi\[x]\[y]



This array stores the amplitude distribution of the decompressed (wave‑like) state.



A compressed state is stored as:



psi\_c\[x] = psi\[x] \* K\[x]^c



Where:



K\[x] is the collapse kernel



c is the compression strength



All arrays are normalized after each operation.



COMPRESSION OPERATION



Compression is implemented as:



psi\_c\[x] = psi\[x] \* K\[x]^c



Where:



c ranges from 0 to 1



K\[x] is a Gaussian‑like kernel centered on the detection region



Kernel definition:



K\[x] = exp( - (x - x0)^2 / (2 \* sigma^2) )



Parameters:



x0    = collapse center



sigma = kernel width



Interpretation:



small sigma  -> strong collapse



large sigma  -> weak collapse



DECOMPRESSION OPERATION



Decompression is the inverse operation:



psi\[x] = psi\_c\[x] / K\[x]^c



This operation is used to simulate:



quantum eraser



partial erasure



recovery of hidden structure



The engine ensures numerical stability by preventing division by zero.



PARTIAL COLLAPSE



Partial collapse is implemented by choosing:



0 < c < 1



This allows simulation of:



weak measurement



partial which‑path marking



partial decoherence



partial erasure



The engine supports continuous values of c for smooth transitions.



MULTI‑PASS COMPRESSION



Sequential compressions are applied multiplicatively:



psi\_c\[x] = psi\[x] \* K1\[x]^c1 \* K2\[x]^c2 \* ...



If kernels are identical:



psi\_c\[x] = psi\[x] \* K\[x]^(c1 + c2 + ...)



The engine tracks:



cumulative compression



hysteresis effects



non‑linear visibility changes



This is essential for testing prediction #7.



COLLAPSE KERNELS



The engine supports multiple kernel types:



Gaussian kernel



Rectangular kernel



Circular kernel (2D)



Asymmetric kernel



Custom user‑defined kernels



Each kernel is defined as a function:



K\[x] -> float



Detector geometry is mapped directly into kernel shape.



VISIBILITY CALCULATION



Interference visibility V is computed as:



V = (I\_max - I\_min) / (I\_max + I\_min)



Where:



I\_max = maximum intensity



I\_min = minimum intensity



The engine computes visibility after:



compression



decompression



multi‑pass operations



detector geometry changes



This is used to test prediction #1.



DISTINGUISHABILITY CALCULATION



Distinguishability D is defined as:



D = c



This is used to test the complementarity rule:



D + V = 1



The engine logs D and V for each simulation run.



TIME‑DEPENDENT COMPRESSION



The engine supports time‑dependent compression:



psi\_c\[x] = psi\[x] \* K\[x]^c \* F(t)



Where F(t) is a decay factor:



F(t) = 1 for t = 0

F(t) < 1 for t > 0



This models prediction #3 (timing sensitivity).



DETECTOR GEOMETRY MAPPING



Detector geometry is mapped into kernel shape.



Examples:



Rectangular detector:

K\[x] = 1 inside region, 0 outside



Circular detector (2D):

K\[x]\[y] = exp( - r^2 / (2 \* sigma^2) )



Asymmetric detector:

K\[x] = exp( - (x - x0)^2 / (2 \* sigma\_left^2) ) for x < x0

K\[x] = exp( - (x - x0)^2 / (2 \* sigma\_right^2) ) for x > x0



The engine uses these kernels to simulate prediction #4.



HIDDEN STRUCTURE RECOVERY



The engine supports reconstruction of hidden structure:



psi\_recovered\[x] = psi\_c\[x] / K\[x]^c



This allows testing prediction #10:



partial collapse preserves recoverable structure



standard QM predicts irreversible loss



ENGINE OUTPUTS



Each simulation run produces:



psi\_before



psi\_after



psi\_recovered (if applicable)



visibility V



distinguishability D



compression c



kernel parameters



detector geometry



time delay (if used)



multi‑pass compression log



Outputs are stored as arrays and metadata dictionaries.



ENGINE ARCHITECTURE



The engine is structured into modules:



state.py



state representation



normalization



amplitude operations



kernel.py



kernel generation



geometry mapping



sigma control



compression.py



compression



decompression



partial collapse



visibility.py



visibility calculation



distinguishability



multipass.py



sequential compression



hysteresis tracking



recovery.py



inverse kernel operations



hidden structure reconstruction



simulation\_engine.py



orchestrates all modules



runs full simulation cycles



SUMMARY



The Simulation Engine implements:



reversible compression



decompression



collapse kernels



detector geometry mapping



visibility and distinguishability



multi‑pass compression



time‑dependent effects



hidden structure recovery



It is the computational foundation of the Information‑Compression Model and is essential for validating predictions and designing experiments.



============================================================

