# 🤖 Tutorial 04 — Basic ML Model (PyTorch)

In this tutorial, you’ll train a **simple neural network** (MLP) with PyTorch to predict an ERA5 variable (default: `t2m`) using the **preprocessed arrays** from Tutorial 03.

You will:
- Load standardized features and targets from `data/processed/`
- Build a small **MLP** (multi-layer perceptron) in PyTorch
- Train with **train/val** loops and **early stopping**
- Evaluate on the **test set** (MSE, RMSE, MAE)
- Visualize the **loss curve** and **Pred vs True** scatter
- Save the trained model and **test predictions**

> **Prerequisites**
> - Completed Tutorial 03 (which creates the `.npy` arrays under `data/processed/`)
> - Environment with `torch`, `numpy`, `matplotlib`
> - Optional GPU will be used automatically if available

## 📓 Notebook
Run everything interactively here:

➡️ **[04_basic_ml_model.ipynb](04_basic_ml_model.ipynb)**

## 📦 Inputs expected (from Tutorial 03)
- `data/processed/X_train.npy`, `X_val.npy`, `X_test.npy` *(already standardized)*
- `data/processed/y_train.npy`, `y_val.npy`, `y_test.npy`
- `data/processed/stats.npz` *(feature scaling stats and lags info)*

## 💾 Outputs (created by the notebook)
- `models/mlp_t2m.pt` (trained PyTorch model)
- `data/processed/y_pred_test.npy` (test predictions)
- `figures/loss_curve.png`
- `figures/pred_vs_true.png`

## ▶️ How to run
From your project root (with your virtual environment activated):

```bash
jupyter notebook  # or: jupyter lab
```

Open the notebook and follow the steps.
