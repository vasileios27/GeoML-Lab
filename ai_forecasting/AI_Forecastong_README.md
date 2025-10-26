Perfect 👍 — here’s a clean and professional **`README.md`** you can add directly to your GeoML-GraphCast repository.
It documents how to run both the FastAPI service and the container, and how to make inference requests using `curl`.

---

# 🌦️ GeoML-GraphCast API

**GeoML-GraphCast** is a containerized FastAPI application that runs DeepMind’s **GraphCast** model for Earth Observation and weather forecasting.
It accepts NetCDF files as input, performs inference, and returns predictions as downloadable NetCDF files.

---

## 🚀 Run the Application

### 🧠 Prerequisites

Make sure you have:

* **Python ≥3.10** and **pip**, or **Docker**
* **FastAPI**, **Uvicorn**, and dependencies installed (via `requirements.txt`)
* The trained GraphCast model files under:

  ```
  app/models/params/
  app/models/stats/
  ```

---

### ▶️ Run Locally (without Docker)

Start the FastAPI app:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ The service will be available at:

```
http://localhost:8000
```

You can check it’s running:

```bash
curl http://localhost:8000/healthz
```

Expected output:

```json
{"status": "ok"}
```

---

### 🐳 Run Inside Docker

If you’ve already built your Docker image (for example `vasileios27/geo_ml_graphcast`):

```bash
docker run --rm -p 8000:8000 vasileios27/geo_ml_graphcast
```

Once started, the API is available at:

```
http://localhost:8000
```

You can also check the live docs in your browser at:

```
http://localhost:8000/docs
```

---

## ⚙️ Example Inference Request

Use the command below to send a **NetCDF input file** and **model name** to the API.

```bash
curl -X POST "http://localhost:8000/echo" \
  -F "model_name=GraphCast_small-ERA5_1979-2015-resolution_1.0-pressure_levels_13-mesh_2to5-precipitation_input_and_output.npz" \
  -F "file=@/home/vvatellis/WeatherData/4castingModels/graphcast/graphcast/data/examples/source-era5_date-2022-01-01_res-1.0_levels-13_steps-04.nc;type=application/netcdf" \
  -o prediction3.nc
```

**Explanation:**

* `model_name`: Selects the model checkpoint to use
* `file`: The input NetCDF file
* `-o prediction3.nc`: Saves the predicted output locally as `prediction3.nc`

---

## 🧩 Folder Structure

```
GeoML_graphcast/
│
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── models/              # Model checkpoints and stats
│   │   ├── params/
│   │   └── stats/
│   └── __init__.py
│
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
└── README.md                # You are here
```

---

## 🧠 Notes

* Input and output formats are **NetCDF (.nc)**
* The `/echo` endpoint runs the model and returns predictions as a `.nc` file
* Typical prediction outputs are stored temporarily and streamed back to the user
* Model checkpoints must be located under `app/models/params/` before running

---

## 🧪 Example Health Check

```bash
curl http://localhost:8000/healthz
```

Expected response:

```json
{"status": "ok"}
```

---

## 🧰 Troubleshooting

| Issue                                                  | Fix                                                                       |
| ------------------------------------------------------ | ------------------------------------------------------------------------- |
| `RuntimeError: Form data requires "python-multipart"`  | Run `pip install python-multipart`                                        |
| `ERROR: Cannot find command 'git'` during Docker build | Add `apt-get install git` to your Dockerfile                              |
| Push rejected by GitHub (file >100MB)                  | Use `.gitignore` or [Git LFS](https://git-lfs.github.com) for large files |

---

## 📄 License

© 2025 Vasileios Vatellis — GeoML-Lab
This project is part of the **GeoML-Lab** initiative for developing AI services in Earth Observation.
