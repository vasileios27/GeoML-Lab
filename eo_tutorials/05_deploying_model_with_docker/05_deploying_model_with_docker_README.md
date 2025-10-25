📁 `05_containerizing_your_AI_model/README.md`

---

# 🐳 Tutorial 05 — Deploying Your EO AI Model with Docker

In this tutorial, you’ll learn how to **containerize** your Earth Observation (EO) machine learning model — that is, how to package your FastAPI-based AI service into a **Docker container** that can be run anywhere.

This tutorial assumes that you already have:

* A working **FastAPI app** that accepts NetCDF input (from Tutorial 04 or earlier)
* Basic familiarity with the **Linux command line**
* Docker installed on your system (`sudo apt install docker.io` or from [docker.com](https://www.docker.com))

---

## 🧠 Learning Objectives

By the end of this tutorial, you will be able to:

1. Create a **FastAPI-based API** that serves predictions from your EO model.
2. Write a **Dockerfile** to containerize your model.
3. Build, run, and test the container locally.
4. Understand how to upload files and retrieve prediction results via API calls.

---

## ⚙️ Step 1 — Project Structure

You should have a directory that looks like this:

```
project_root/
│
├── app/
│   ├── main.py          ← FastAPI app (defines /predict or /echo endpoint)
│   └── models/          ← Your model files/checkpoints
│
├── requirements.txt     ← Python dependencies
├── Dockerfile           ← Instructions to build your container
└── sample_input.nc      ← Example NetCDF file for testing
```

---

## 🚀 Step 2 — Create the FastAPI Service

Your main service file (`app/main.py`) defines a simple API that:

1. Accepts a **NetCDF file** and a **model name**
2. Runs your model on the input
3. Returns the **prediction** as a downloadable NetCDF file

Example structure:

```python
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
import tempfile, os, xarray as xr

app = FastAPI(title="EO Model API", version="0.1")

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(
    model_name: str = Form(...),
    file: UploadFile = File(...),
):
    # 1️⃣ Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmp_in:
        contents = await file.read()
        tmp_in.write(contents)
        upload_path = tmp_in.name

    try:
        # 2️⃣ Load and preprocess NetCDF data (your model logic goes here)
        ds = xr.open_dataset(upload_path)

        # 3️⃣ Dummy "prediction" (for testing)
        pred = ds.mean(dim="time")

        # 4️⃣ Save output NetCDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmp_out:
            output_path = tmp_out.name
        pred.to_netcdf(output_path, engine="netcdf4")

        # 5️⃣ Return as downloadable file
        background = BackgroundTasks()
        background.add_task(lambda p: os.remove(p), output_path)
        return FileResponse(output_path, filename=f"{model_name}_prediction.nc", background=background)

    finally:
        os.remove(upload_path)
```

👉 Once your model code is ready, you can replace the “dummy” prediction with real inference.

---

## 📦 Step 3 — Create a Requirements File

Export your environment’s dependencies into a `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

Make sure it includes essential packages such as:

```
fastapi
uvicorn[standard]
xarray
netCDF4
python-multipart
```

If your model uses external libraries (e.g., PyTorch, TensorFlow, or JAX), add them as well.

---

## 🐋 Step 4 — Write the Dockerfile

Create a file named `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

# Install system dependencies (git required for GraphCast or similar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app
COPY app ./app

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🏗️ Step 5 — Build the Docker Image

Run this command in the same folder as your `Dockerfile`:

```bash
docker build -t eo_model_api .
```

This will:

1. Pull the Python base image
2. Install dependencies
3. Copy your code into the image
4. Build a reusable, portable environment

---

## ▶️ Step 6 — Run the Container

Start the container and expose port 8000 to your host:

```bash
docker run --rm -p 8000:8000 eo_model_api
```

If successful, you’ll see logs like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧪 Step 7 — Test the API

### ✅ Health check

```bash
curl http://localhost:8000/healthz
```

Expected output:

```json
{"status":"ok"}
```

### 📤 Send a NetCDF file

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "model_name=test_model" \
  -F "file=@sample_input.nc;type=application/netcdf" \
  -o prediction_output.nc
```

This uploads your input file and downloads the model’s prediction as `prediction_output.nc`.

---

## 🧼 Step 8 — Stop and Clean Up

To stop the container, press **Ctrl + C**.
To remove old containers or images:

```bash
docker ps -a
docker rm <container_id>
docker rmi eo_model_api
```

---

## 🎯 What You’ve Learned

In this tutorial, you learned how to:

1. Build a **FastAPI service** to wrap your EO model.
2. Package it inside a **Docker container**.
3. Run and test the API locally using `curl`.
4. Return prediction outputs in NetCDF format.

---

## 🪐 Next Steps

In future tutorials, we’ll explore:

* Deploying your containerized model to the cloud (e.g., AWS or Azure)
* Using async job queues for large EO workloads
* Creating front-end dashboards to visualize model results in real time
