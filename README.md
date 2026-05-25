\# Double‑Slit Information‑Physics Engine  

\### Wave ↔ Particle via Information Compression



This project is an open‑source physics engine that simulates the double‑slit experiment using a new conceptual model:



\*\*Wave = decompressed information\*\*  

\*\*Particle = compressed information\*\*



Instead of treating wave/particle duality as a mystery, this engine models it as an \*\*information‑state transition\*\* driven by measurement, detectors, and information availability.



The result is a fully visual, dynamic simulation showing:



\- wave propagation  

\- interference  

\- detector‑driven compression  

\- particle‑like Gaussian packets  

\- directional propagation  

\- probabilistic collapse  

\- re‑decompression (information removal)  

\- continuous state‑map overlays  



This is the most detailed, instrumented, open‑source visualization of information‑driven wave/particle transitions.



\---



\## ⭐ Features



\### \*\*Wave Mode (Decompressed Information)\*\*

\- Full complex wavefunction ψ(x, y)  

\- Interference and superposition  

\- Schrödinger‑like propagation  

\- LOD (level‑of‑detail) rendering  



\### \*\*Particle Mode (Compressed Information)\*\*

\- Localized Gaussian packet  

\- Directional propagation  

\- No interference  

\- State map = 1.0  



\### \*\*Information‑State Map (0 → 1)\*\*

\- 0.0 = pure wave  

\- 0.5 = partial information / decoherence  

\- 1.0 = full particle  



\### \*\*Detectors\*\*

\- Left and right slit detectors  

\- Independent triggering  

\- Probabilistic collapse  

\- Partial‑strength compression  



\### \*\*Re‑Decompression (Information Removal)\*\*

\- Wavefront re‑expands  

\- Interference returns  

\- State map resets  



\### \*\*Visualization\*\*

\- Multi‑stage overlays  

\- State‑map transparency layer  

\- Particle center markers  

\- Event logging  



\---



\## ⭐ Theory Summary



This engine is based on a simple but powerful idea:



> \*\*Information determines physical form.\*\*  

>  

> When information is \*decompressed\*, the system behaves like a wave.  

> When information is \*compressed\*, the system behaves like a particle.  

>  

> Measurement = compression  

> Information removal = re‑decompression  



This model reproduces:



\- wave behavior  

\- particle behavior  

\- collapse  

\- decoherence  

\- quantum eraser effects  



All using \*\*information state\*\*, not hidden variables or randomness alone.



\---



\## ⭐ Project Structure

doubleslit/
│
├── engine/
│   ├── wave_engine.py
│   └── init.py
│
├── experiments/
│   ├── double_slit.py
│   └── init.py
│
├── examples/
│   ├── screenshots/
│   └── README.md
│
├── LICENSE
├── README.md
└── requirements.txt




---

## ⭐ Installation

pip install numpy matplotlib


---

## ⭐ Running the Simulation

python experiments/double_slit.py


This will generate:

- `double_slit_full_info_physics_engine.png`  
- event logs  
- state‑map overlays  

---

## ⭐ Contributing

Pull requests are welcome.

Ideas worth exploring:

- multi‑particle interactions  
- entanglement via shared information state  
- 3D extension  
- GPU acceleration  
- real‑time viewer  

---

## ⭐ License

This project is released under the **MIT License** (see LICENSE file).

---

## ⭐ Author

Thomas Price  
Crestwood, KY  
2026

# Quantum Slow‑Motion Visualization

This project generates a **40‑second slow‑motion visualization** of a single quantum particle transforming smoothly between:

- **Compressed particle**
- **Decompressed wave**
- **Collapse under observation**
- **Re‑expansion when observation ends**

The entire animation is rendered as **one continuous shot** with:

- Fixed camera  
- Soft teal volumetric glow  
- Smooth transitions  
- Centered captions that fade in/out  
- Detector visualization  
- 720p output  

The final result is saved as:
quantum_slow_motion.mp4


---

## 🔧 Requirements

You need:

### **1. Python 3.9+**
Download from: https://www.python.org/downloads/

### **2. Python packages**
Install them with:
pip install numpy matplotlib


### **3. FFmpeg (required to build the MP4)**
Download Windows builds here:

https://www.gyan.dev/ffmpeg/builds/

After downloading:
- Extract the folder  
- Add the `bin` folder to your **PATH**  
- Confirm installation:

ffmpeg -version


If FFmpeg is not installed, the script will still render PNG frames, but will not create the MP4.

---

## ▶️ Running the Simulation

Run the script:
py quantum_slow_motion.py

The script will:

1. Generate all frames in a folder  
2. Use FFmpeg to assemble them into `quantum_slow_motion.mp4`  
3. Delete the PNG frames after the video is created  

When finished, open the MP4 with VLC or any video player.

---

## 📜 What the Video Shows

The animation visualizes:

1. **Particle emission**  
2. **Forward motion while compressed**  
3. **Smooth decompression into a wave**  
4. **Detector observing the wave**  
5. **Instant collapse back into a particle**  
6. **Observation ending**  
7. **Re‑expansion into a wave**  
8. **Free wave evolution**

Captions appear centered with smooth fade‑in/fade‑out transitions.

---

## 📁 File Structure
quantum_slow_motion.py

README.md


The script creates temporary frames in:
frames_quantum/

This folder is automatically removed after the MP4 is built.

---

## 🧠 Purpose

This visualization is designed to show:

- Compression vs. decompression  
- Observation vs. no‑observation  
- Wavefunction behavior  
- Collapse events  
- Smooth quantum evolution in slow motion  

It is a teaching and demonstration tool for quantum behavior and information‑compression concepts.

---

## ✔️ License

MIT License (or choose your own)




