## building the environment
### step1: creating virtual environment

```
ml purge
ml load miniconda3/24.11.1
conda create -n FCNV3_env python=3.12
```
## load in the environment

```
conda activate FCNV3_env
```

### step2: loading the module FCNV3 need from nano5
### loading gcc and cuda
### appendix: module spider # module list
```
ml load gcc/11.5.0
ml load cuda/12.6
```

### step3: downloading the makani and building the environment
### makani github: https://github.com/NVIDIA/makani
```
git clone https://github.com/NVIDIA/makani.git
cd makani
pip install -e .
```
### adding other package
```
pip install ruamel.yaml moviepy scipy matplotlib
pip install xarray pygrib cfgrib netCDF4
```
## after finishing please cheak the torch with cuda:
## it will be True, if cuda is available
```
python - << 'EOF'
import torch
print(torch.__version__)
print("torch cuda:", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
EOF
```

###　build torch-horminco
### make the environment clear
```
pip uninstall -y torch-harmonics
pip cache purge
```
### add the export
```
export FORCE_CUDA_EXTENSION=1
```
### then install torch-harmonics (it will be in long time...)
```
pip install -v --no-build-isolation --no-cache-dir --no-binary torch-harmonics torch-harmonics
```

## removing some WARNING
```
pip uninstall -y pynvml
pip install -U nvidia-ml-py
```

## the weight of FCNV3
https://catalog.ngc.nvidia.com/orgs/nvidia/teams/earth-2/models/fourcastnet3?version=0.1.0
```
mkdir FCNV3_weight
cd mkdir FCNV3_weight

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=config.json' --output-document 'config.json'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=global_means.npy' --output-document 'global_means.npy'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=global_stds.npy' --output-document 'global_stds.npy'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=land_mask.nc' --output-document 'land_mask.nc'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=maxs.npy' --output-document 'maxs.npy'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=metadata.json' --output-document 'metadata.json'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=mins.npy' --output-document 'mins.npy'

wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=orography.nc' --output-document 'orography.nc'

mkdir training_checkpoints
cd training_checkpoints
wget --content-disposition 'https://api.ngc.nvidia.com/v2/models/org/nvidia/team/earth-2/fourcastnet3/0.1.0/files?redirect=true&path=training_checkpoints/best_ckpt_mp0.tar' --output-document 'best_ckpt_mp0.tar'

cd ../../
```


### now can run the FCNV3
```
sbatch run_FCNV3_test.sh
```
### detail for running python FCNV3
```
python download_history_ncep.py --scheduled-time 2025091800

python FCNV3_inference.py --input_data input_data/ncep_initial_condition.npy --input_time 2025091800 --output_folder output_FCNV3_2025091800 --fore_hr 72

python FCNV3_inference_ens.py --input_data input_data/ncep_initial_condition.npy --input_time 2025091800 --output_folder output_FCNV3_2025091800_ens1  --fore_hr 72
```
