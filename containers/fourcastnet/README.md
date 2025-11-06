# FourCastNet — Installation & Local Execution Guide
## **1. GPU Environment**

This environment is configured for **GPU acceleration** using:

* **CUDA Toolkit:** `12.8`
* **cuDNN:** `9.14.0`

These versions are compatible with **Python 3.10**, **JAX**, and **PyTorch ≥ 2.2**, ensuring optimal performance and model stability for GraphCast and other deep learning workloads.

#### 🧰 Installation Notes

If your system does not already include the correct NVIDIA drivers and CUDA libraries, you can install them manually.

Official installation instructions and downloadable packages are available at:
👉 [**NVIDIA CUDA Download Page (Ubuntu 24.04, x86_64)**](https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04)
## 1. Environment setup
```bash
# Create a virtual environment named "graphcast" using Python 3.10
python3.10 -m venv env_fourecastnet
# Activate the environment
source env_fourecastnet/bin/activate      # on Linux or macOS

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
 
## 2. Model checkpoints www

The full instractions of ai-models from ECMWF can be found in the link below.
👉 [**ai-models from ECMWF**](https://github.com/ecmwf-lab/ai-models)

Download pretrained params and stats:
```bash
pip install ai-models
pip install ai-models-fourecastnet
```

```bash
ai-models --download-assets --assets ./assets fourecastnet
```

## 3. Running inference

```bash

```