# Slurm Notes for Nano5 (TWCC)

This document provides a brief reference for using **Slurm** on **Nano5 (TWCC)**,
based on the official manual.

Reference: https://man.twcc.ai/@AI-Pilot/manual

---

## Submitting Jobs with `sbatch`

Below is a basic example of a Slurm batch script (`sample-job.sh`):

```bash
#!/bin/bash
#SBATCH --account=<PROJECT_ID>          # (-A) iService Project ID
#SBATCH --job-name=<JOB_NAME>           # (-J) Job name
#SBATCH --partition=dev                 # (-p) Partition (dev, normal, normal2, 4nodes)
#SBATCH --nodes=1                       # (-N) Number of nodes
#SBATCH --gpus-per-node=1               # GPUs per node
#SBATCH --cpus-per-task=4               # (-c) CPU cores per task
#SBATCH --time=02:00:00                 # (-t) Wall time limit (HH:MM:SS, depends on partition)
#SBATCH --output=job_logs/job-%j.out    # Standard output log
#SBATCH --error=job_logs/job-%j.err     # Standard error log
#SBATCH --mail-type=END,FAIL            # Mail notification type
#SBATCH --mail-user=your_email@domain   # Email for notifications
```

Submit the job:

```bash
sbatch sample-job.sh
```

---

## Checking Job Status

### Check all jobs in the system

```bash
squeue
```

### Check only your jobs

```bash
squeue -u $UID
```

---

## Login to Compute Node and Cancel Jobs

### Login to an allocated compute node

```bash
ssh <NODELIST>
```

> `<NODELIST>` can be found in the output of `squeue`.

### Cancel a job

```bash
scancel <JOB_ID>
```

---

## Running Interactive Jobs

To request an interactive allocation (commonly used for debugging):

```bash
salloc --partition=dev --account=<PROJECT_ID> --ntasks=1 --gpus-per-node=1
```

After allocation, you will be placed directly on the compute node.

---

## Notes

- Always make sure the selected **partition** matches your requested wall time.
- Use the `dev` partition for short test jobs and debugging.
- Remember to cancel unused jobs to release resources.

For detailed and up-to-date information, please refer to the official TWCC Nano5 manual.
