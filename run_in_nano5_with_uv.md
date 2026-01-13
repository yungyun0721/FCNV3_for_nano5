# FCNV3 Environment Setup with `uv` (Nano5)

This document describes how to build a Python environment using **uv** to run **FCNV3**
on Nano5, including dependency installation, CUDA verification, weight download,
and inference execution.

---

## Install `uv`

### Download `uv` and add it to `.bashrc`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Download this repository 

```bash
cd /work/<username>/
git clone https://github.com/yungyun0721/FCNV3_for_nano5.git
cd FCNV3_for_nano5
```

## Build the Environment

### Step 1 — Create a virtual environment

Go to the FCNV3 working directory:

```bash
cd FCNV3_test
uv venv FCNV3_env
```

Activate the environment:

```bash
source FCNV3_env/bin/activate
```

---

### Step 2 — Load required system modules (Nano5)

```bash
ml purge
ml load gcc/11.5.0
ml load cuda/12.6
```

> Tip: use `module spider <name>` to check available module versions.

---

### Step 3 — Install Makani and dependencies

Makani GitHub repository:  
https://github.com/NVIDIA/makani

```bash
git clone https://github.com/NVIDIA/makani.git
uv pip install -e ./makani/
```

Install additional Python packages:

```bash
uv pip install ruamel.yaml moviepy scipy matplotlib
uv pip install xarray pygrib cfgrib netCDF4
```

---

## Verify PyTorch and CUDA

After installation, check whether PyTorch detects CUDA:

```bash
python - << 'EOF'
import torch
print("torch version:", torch.__version__)
print("torch cuda:", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
EOF
```

### Install PyTorch manually (if not installed)

Refer to: https://pytorch.org/get-started/previous-versions/

```bash
pip install torch==2.9.0 torchvision==0.24.0 torchaudio==2.9.0 \
  --index-url https://download.pytorch.org/whl/cu126
```

---

## Build `torch-harmonics` (CUDA extension)

### Clean existing installation

```bash
uv pip uninstall torch-harmonics
```

### Force CUDA extension build

```bash
export FORCE_CUDA_EXTENSION=1
```

### Install `torch-harmonics` (this may take a long time)

```bash
uv pip install -v --no-build-isolation --no-cache-dir --no-binary torch-harmonics torch-harmonics
```

---

## Fix NVML Warnings (Optional)

```bash
uv pip uninstall pynvml
uv pip install -U nvidia-ml-py
```

---

## Download FCNV3 Weights

Model page (NVIDIA NGC):  
https://catalog.ngc.nvidia.com/orgs/nvidia/teams/earth-2/models/fourcastnet3?version=0.1.0

Create the weight directory:

```bash
mkdir -p FCNV3_weight
cd FCNV3_weight
```

Download configuration, statistics, and static fields:

```bash
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=config.json' --output-document 'config.json'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=global_means.npy' --output-document 'global_means.npy'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=global_stds.npy' --output-document 'global_stds.npy'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=land_mask.nc' --output-document 'land_mask.nc'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=maxs.npy' --output-document 'maxs.npy'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=metadata.json' --output-document 'metadata.json'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=mins.npy' --output-document 'mins.npy'
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=orography.nc' --output-document 'orography.nc'
```

Download training checkpoint:

```bash
mkdir -p training_checkpoints
cd training_checkpoints

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=training_checkpoints/best_ckpt_mp0.tar' --output-document 'best_ckpt_mp0.tar'

cd ../../
```

---

## Run FCNV3

### Submit job on Nano5

```bash
sbatch run_FCNV3_test_uv.sh
```

---

## Run FCNV3 Manually (Example Commands)

```bash
python download_history_ncep.py --scheduled-time 2025091800
```

Deterministic inference:

```bash
python FCNV3_inference.py \
  --input_data input_data/ncep_initial_condition.npy \
  --input_time 2025091800 \
  --output_folder output_FCNV3_2025091800 \
  --fore_hr 72
```

Ensemble inference:

```bash
python FCNV3_inference_ens.py \
  --input_data input_data/ncep_initial_condition.npy \

  --input_time 2025091800 \
  --output_folder output_FCNV3_2025091800_ens1 \
  --fore_hr 72
```

---
