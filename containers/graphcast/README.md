# GraphCast — Installation & Local Execution Guide

## 1. Environment setup
```bash
# Create a virtual environment named "graphcast" using Python 3.10
python3.10 -m env_graphcast
# Activate the environment
source env_graphcast/bin/activate      # on Linux or macOS

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
pip install ai-models-graphcast
```
Install GraphCast from git
```bash
git clone https://github.com/google-deepmind/graphcast.git
pip install -e /home/vasileios_vatelis/GeoML/GeoML_graphcast/graphcast/
```

```bash
ai-models --download-assets --assets ./assets graphcast
```