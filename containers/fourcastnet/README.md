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
 
## 2. Model checkpoints 

The full instractions of ai-models from ECMWF can be found in the link below.
👉 [**ai-models from ECMWF**](https://github.com/ecmwf-lab/ai-models)

Download pretrained params and stats:
```bash
pip install ai-models
pip install ai-models-fourecastnet
```
make a directory and save the "assets", which are the models checjpoints and other requierd files for the model,
then use the command below to dowload the files
```bash
ai-models --download-assets --assets ./assets fourecastnet
```

Perfect — let’s go through this cleanly, step-by-step 👇
This will show you **where Earthkit saves data now**, and then how to **change it permanently** to a custom folder (for example on `/mnt/disks/GeoML/earthkit_data`).

---

## 3 — Check current Earthkit cache location

Run this in your terminal:

```bash
python -c "import earthkit.data as ekd; print(ekd.settings.get('user-cache-directory'))"
```

Example output:

```bash
/tmp/earthkit-data-vasileios
```

That’s your **current cache directory** (where Earthkit stores downloaded `.cache` or `.grib` files).

---

Choose a location on your larger disk, e.g. `/mnt/disks/GeoML/earthkit_data`, and make sure it exists and is writable:

```bash
mkdir -p /mnt/disks/GeoML/earthkit_data
chmod -R u+rwX /mnt/disks/GeoML/earthkit_data
```

---

### I — Temporarily change it (for the current session only)

You can override it at runtime to test:

```bash
python -c "import earthkit.data as ekd; ekd.settings.set('user-cache-directory','/mnt/disks/GeoML/earthkit_data'); print(ekd.settings.get('user-cache-directory'))"
```

Output should confirm:

```
/mnt/disks/GeoML/earthkit_data
```

⚠️  This works only **while Python is running** — next time you start Python, it resets.

---

### II — Make the change permanent (edit config file)

Earthkit reads its configuration from:

```
~/.config/earthkit/data/config.yaml
```

Open or create it:

```bash
nano ~/.config/earthkit/data/config.yaml
```

Paste this minimal valid YAML (edit version if needed):

```yaml
version: "0.17.0"
cache-policy: user
user-cache-directory: "/mnt/disks/GeoML/earthkit_data"
maximum-cache-disk-usage: "95%"
```

Save (Ctrl + O, Enter) and exit (Ctrl + X).

---

### III — Verify it’s active

Run again:

```bash
python -c "import earthkit.data as ekd; [print(line) for line in ekd.settings.dump()]"
```

You should see a line like:

```
('user-cache-directory', '/mnt/disks/GeoML/earthkit_data', ...)
```

That confirms Earthkit will now **always save all data** (CDS downloads, GRIB files, etc.) in your specified folder.


## 4. Running inference

```bash

```