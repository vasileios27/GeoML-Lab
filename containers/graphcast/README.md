## 🧠 GraphCast Local Setup (Stable Python 3.10 / JAX 0.6.0 Environment)

This environment is configured for **GPU acceleration** using:

* **CUDA Toolkit:** `12.8`

These versions are compatible with **Python 3.10**, **JAX**, and **PyTorch ≥ 2.2**, ensuring optimal performance and model stability for GraphCast and other deep learning workloads.

#### 🧰 Installation Notes

If your system does not already include the correct NVIDIA drivers and CUDA libraries, you can install them manually.

Official installation instructions and downloadable packages are available at:
👉 [**NVIDIA CUDA Download Page (Ubuntu 24.04, x86_64)**](https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04)
This README documents the installation steps and requirements for running **GraphCast** with **ai-models** in a stable Python 3.10 environment.

### ⚙️ 1. Create and Activate Environment

```bash
# From your project root
python3 -m venv env_graphcast
source env_graphcast/bin/activate
```

### 📦 2. Install Core Dependencies (Pinned for Compatibility)

Create a file called `constraints.txt` with the following content:

```txt
jax==0.6.0
jaxlib==0.6.0
jax-cuda12-plugin==0.6.0
jax-cuda12-pjrt==0.6.0
dm-haiku==0.0.10
chex==0.1.90
optax==0.2.4
numpy==1.26.4
scipy==1.15.3
ai-models==0.7.4
ai-models-graphcast==0.1.0
```

Then install with:

```bash
pip install --force-reinstall -r constraints.txt
```

> 💡 *All packages are pinned to maintain compatibility with JAX 0.6.0 and Python 3.10.*

---

### 📚 3. Install GraphCast (from source, no dependency changes)

Clone and install GraphCast in **editable mode** without dependencies:

```bash
cd ~/GeoML/GeoML_graphcast
git clone https://github.com/google-deepmind/graphcast.git
cd graphcast
pip install --no-deps -e .
```

---

### 🧩 4. Install Missing Runtime Packages (No-Dependency Mode)

Some submodules require additional lightweight libraries. Install them safely:

```bash
pip install --no-deps jraph==0.0.6.dev0
pip install --no-deps trimesh==3.23.5
```

---

### 🧪 5. Verify the Installation

Run the following test:

```bash
python - <<'PY'
import importlib, jraph, trimesh, graphcast
print("jraph ok:", jraph.__version__)
print("trimesh ok:", trimesh.__version__)
m = importlib.import_module("graphcast.graphcast")
print("graphcast.graphcast ok:", m.__file__)
PY
```

Expected output:

```
jraph ok: 0.0.6.dev0
trimesh ok: 3.23.5
graphcast.graphcast ok: /.../graphcast/graphcast/graphcast.py
```

---

### 🌍 6. Download GraphCast Assets via ai-models

```bash
ai-models --download-assets --assets ./assets graphcast
```

> If you see `INFO Total time: ... seconds` with no errors, your setup is complete.

---

### 🧾 Notes

* Python version: **3.10**
* CUDA: **12.x**
* JAX stack: **0.6.0**
* ai-models: **0.7.4**
* GraphCast: **editable install** (from local repo)
* No package upgrades beyond the pinned list

---

Would you like me to include an **environment.yml** (for conda) or a **requirements.txt** that mirrors the pinned setup from this README? That would make your setup reproducible on another machine (e.g., Google Cloud or HPC).
