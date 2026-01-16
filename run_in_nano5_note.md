# FCNV3 Environment Setup and Inference Guide (Nano5)

This document describes how to build the FCNV3 environment on Nano5 using Conda,
install required dependencies (Makani, torch-harmonics), download FCNV3 weights,
and run inference jobs.

---

## Download this repository 

```bash
cd /work/<username>/
git clone https://github.com/yungyun0721/FCNV3_for_nano5.git
cd FCNV3_for_nano5
```

## Build the Environment with Conda

### Step 1 — Create the conda environment

```bash
ml purge
ml load miniconda3/24.11.1

conda create -n FCNV3_env python=3.12 -y
conda activate FCNV3_env
```

---

### Step 2 — Load required system modules (gcc / cuda)

> Tip: Use `module spider <name>` to check available module versions.

```bash
ml load gcc/11.5.0
ml load cuda/12.6
```

---

### Step 3 — Clone Makani and install dependencies

Makani GitHub repository:  
https://github.com/NVIDIA/makani

```bash
git clone https://github.com/NVIDIA/makani.git
pip install -e ./makani/
```

Install additional Python packages:

```bash
pip install ruamel.yaml moviepy scipy matplotlib
pip install xarray pygrib cfgrib netCDF4
```

---

### Step 4 — Verify PyTorch CUDA availability

CUDA should be available (`True`) if the environment is set correctly.

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

### Clean old installation and cache (recommended)

```bash
pip uninstall -y torch-harmonics
pip cache purge
```

### Force CUDA extension build

```bash
export FORCE_CUDA_EXTENSION=1
```

### Install torch-harmonics (this may take a long time)

```bash
pip install -v --no-build-isolation --no-cache-dir --no-binary torch-harmonics torch-harmonics
```

---

## Fix NVML Warning (Optional)

If you encounter NVML-related warnings:

```bash
pip uninstall -y pynvml
pip install -U nvidia-ml-py
```

---

## Download FCNV3 Weights

Model page (NVIDIA NGC):  
https://catalog.ngc.nvidia.com/orgs/nvidia/teams/earth-2/models/fourcastnet3?version=0.1.0

Create weight directory:

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

## Run FCNV3 on Nano5

Submit the batch job:

```bash
sbatch run_FCNV3_test.sh
```

---

## Run FCNV3 Manually (Example Commands)

You can modify these commands inside `run_FCNV3_test.sh` if needed.

```bash
python download_history_ncep.py --scheduled-time 2025091800
# or
python download_IFS.py --scheduled-time 2025091800
```

Run deterministic inference:

```bash
python FCNV3_inference.py \
  --input_data input_data/ncep_initial_condition.npy \
  --input_time 2025091800 \
  --output_folder output_FCNV3_2025091800 \
  --fore_hr 72
```

Run ensemble inference:

```bash
python FCNV3_inference_ens.py \
  --input_data input_data/ncep_initial_condition.npy \
  --input_time 2025091800 \
  --ens_mem 5\
  --output_folder output_FCNV3_2025091800_ens \
  --fore_hr 72
```

Run plot850.py:

```bash
python plot850.py \
  -f output_FCNV3_2025091800 \
  -o plot_2025091800
```
