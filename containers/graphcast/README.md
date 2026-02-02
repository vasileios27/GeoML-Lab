## 🧠 GraphCast Local Setup (Stable Python 3.10 / JAX 0.6.0 Environment)

This environment is configured for **GPU acceleration** using:

* **CUDA Toolkit:** `12.8`

These versions are compatible with **Python 3.10**, **JAX**, and **PyTorch ≥ 2.2**, ensuring optimal performance and model stability for GraphCast and other deep learning workloads.

#### 🧰 Installation Notes

If your system does not already include the correct NVIDIA drivers and CUDA libraries, you can install them manually.

Official installation instructions and downloadable packages are available at:
👉 [**NVIDIA CUDA Download Page (Ubuntu 24.04, x86_64)**](https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04)
This README documents the installation steps and requirements for running **GraphCast** with **ai-models** in a stable Python 3.10 environment.

# GraphCast Installation README

This README summarizes all steps taken to successfully install **GraphCast**, **ai-models**, and the supporting libraries in the custom environment `env_graphcast`.

---

## 1. Create and Activate the Python Environment

A dedicated environment was created to isolate GraphCast, JAX, and AI Models.

```bash
python3 -m venv env_graphcast
source env_graphcast/bin/activate
```

---

## 2. Install JAX with CUDA 12 Support

We installed JAX and JAXLIB manually to match the system GPU setup.

```bash
pip install --upgrade "jax[cuda12]" --find-links https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

After installation, device availability was tested:

```bash
python3 -c "import jax; print(jax.devices())"
```

We fixed CUDA library issues by ensuring `LD_LIBRARY_PATH` was **unset** so JAX could correctly detect system CUDA libs:

```bash
unset LD_LIBRARY_PATH
```

The GPU detection succeeded afterwards.

---

## 3. Install Haiku

DeepMind's Haiku library is required by GraphCast.

Compatible version:

```bash
pip install git+https://github.com/deepmind/dm-haiku
```

Verification:

```bash
python3 -c "import haiku as hk; print('Haiku OK')"
```

---

## 4. Install GraphCast (without dependencies)

GraphCast was installed manually without dependencies to avoid overwriting JAX.

```bash
pip install git+https://github.com/google-deepmind/graphcast.git --no-deps
```

Dependencies were added manually later.

---

## 5. Install ai-models and ai-models-graphcast

These packages integrate GraphCast into the ECMWF `ai-models` system.

Installed without dependencies:

```bash
pip install ai-models --no-deps
pip install ai-models-graphcast --no-deps
```

---

## 6. Install Required Dependencies Manually

The `ai-models` package reported missing dependencies, which we installed one by one:

### Required ECMWF/GraphCast dependencies

```bash
pip install cdsapi
pip install earthkit-data
pip install earthkit-regrid
pip install ecmwf-api-client
pip install ecmwf-opendata\pip install gputil\pip install dm-tree
pip install matplotlib
```

Some required system libraries were also installed for packages like `cartopy` and `rtree`.

---

## 7. Fix NumPy Version Compatibility

`ai-models` requires `numpy < 2`, so we downgraded:

```bash
pip install "numpy<2" --upgrade
```

---

## 8. Configure Earthkit Cache Directory

We configured a custom cache directory by creating:

```
~/.config/earthkit/config.yaml
```

With contents:

```yaml
data:
  cache_dir: "/mnt/disks/GeoML/earthkit_cache"
  archive_dir: "/mnt/disks/GeoML/earthkit_data"
```

This ensures Earthkit stores data on the mounted disk.

---

## 9. Locating and Understanding ai-models GraphCast Runner

We explored the installed package to enable customization:

```
/path/to/env_graphcast/lib/python3.12/site-packages/ai_models_graphcast/model.py
```

This file contains the GraphCast model wrapper, JAX execution, and all logic executed when running:

```bash
ai-models graphcast ...
```

This is the correct file to modify if enabling custom GPU logic or multi-GPU usage.

---

## 10. Running GraphCast

Typical example:

```bash
ai-models --assets ./assets/ --input cds --date 20230110 --time 0000 --lead-time 24 graphcast
```

If needed, a specific GPU can be selected via:

```bash
CUDA_VISIBLE_DEVICES=1 ai-models ... graphcast
```

---

## Installation Completed

At this point, GraphCast, ai-models, and all auxiliary dependencies are installed and working in the `env_graphcast` environment.

Further customization (e.g., multi-GPU execution) can now be performed directly in:

```
ai_models_graphcast/model.py
```
