#!/bin/bash
#SBATCH --account=MST114049           # (-A) iService Project ID
#SBATCH --job-name=FCNV3_test         # (-J) Job name
#SBATCH --partition=dev               # (-p) Slurm partition
#SBATCH --gpus-per-node=1             # Gpus per node
#SBATCH --cpus-per-task=4
#SBATCH --time=02:00:00               # (-t) Wall time limit (days-hrs:min:sec)
#SBATCH --output=job_logs/job-%j.out           # (-o) Path to the standard output file
#SBATCH --error=job_logs/job-%j.err            # (-e) Path to the standard error file
#SBATCH --mail-type=END,FAIL          # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=carol8351119@gmail.com  # Where to send mail.  Set this to your email address


date
ml load miniconda3/24.11.1  
ml load gcc/11.5.0 
ml load cuda/12.4
conda activate FCNV3_env
ml list

export CC=/work/HPC_software/LMOD/gcc/11/bin/gcc
export CXX=/work/HPC_software/LMOD/gcc/11/bin/g++
export CUDA_HOME=$(dirname $(dirname $(which nvcc)))   # 會指到 .../cuda-12.6
unset CFLAGS CXXFLAGS CPPFLAGS
export FORCE_CUDA_EXTENSION=1
export TORCH_CUDA_ARCH_LIST="9.0"   # H100 = SM90

# Run download data
python download_history_ncep.py --scheduled-time 2025091800

# Run determine FCNV3 run
python FCNV3_inference.py \
	--input_data input_data/ncep_initial_condition.npy \
	--input_time 2025091800 \
	--output_folder output_FCNV3_2025091800\
    --fore_hr 96

# python FCNV3_inference_ens.py \
# 	--input_data input_data/ncep_initial_condition.npy\
#   --input_time 2025091800\
#   --ens_mem 5\
#   --output_folder output_FCNV3_2025091800_ens \
# 	--fore_hr 96

# python plot850.py \
#   -f output_FCNV3_2025091800 \
#   -o plot_2025091800

echo "Finshing..."
date
