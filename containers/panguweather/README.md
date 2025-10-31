# Ppangu-Weather — Installation & Local Execution Guide

## **1. GPU Environment**

This environment is configured for **GPU acceleration** using:

* **CUDA Toolkit:** `12.8`
* **cuDNN:** `9.14.0`

These versions are compatible with **Python 3.10**, **JAX**, and **PyTorch ≥ 2.2**, ensuring optimal performance and model stability for GraphCast and other deep learning workloads.

#### 🧰 Installation Notes

If your system does not already include the correct NVIDIA drivers and CUDA/cuDNN libraries, you can install them manually.

Official installation instructions and downloadable packages are available at:
👉 [**NVIDIA CUDA Download Page (Ubuntu 24.04, x86_64)**](https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04)
👉 [**NVIDIA cuDNN Download Page (Ubuntu 24.04, x86_64)**](https://developer.nvidia.com/cudnn-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_local&Configuration=Full)



#### ✅ Verify Installation

```bash
nvidia-smi
nvcc --version
```

Both commands should confirm CUDA 12.8 and a working GPU driver.

---

Would you like me to now generate the **full `containers/graphcast/README.md`** using this section — including the Python 3.10 venv setup, CUDA/cuDNN note, checkpoint download, and common troubleshooting tips?

## 1. Environment setup

For this enviroment we use CUDA Version: 12.8, and cuDNN 9.14.0

Installation instractions and files can be found
```bash 

https://developer.nvidia.com/cudnn-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=24.04&target_type=deb_local&Configuration=Full
```


```bash
# Create a virtual environment named "graphcast" using Python 3.10
python3.10 -m env_panguweather
# Activate the environment
source env_panguweather/bin/activate      # on Linux or macOS

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Model checkpoints

Download pretrained params and stats:
```bash

```

## 3. Running inference

```bash

```