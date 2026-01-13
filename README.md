# FCNV3 on Nano5 (Taiwan HPC)

## Repository Overview

This repository provides a practical guide for running **FourCastNet v3 (FCNV3)** on **Nano5**,  
the Taiwan High Performance Computing (HPC) system.

The implementation and workflow are based on NVIDIA’s **Earth2Studio**, **Makani**, and the
official **FourCastNet-3** references:

- Earth2Studio: https://github.com/NVIDIA/earth2studio  
- Makani: https://github.com/NVIDIA/makani  
- FourCastNet-3 technical blog:  
  https://developer.nvidia.com/blog/fourcastnet-3-enables-fast-and-accurate-large-ensemble-weather-forecasting-with-scalable-geometric-ml/

---

## Purpose

This repository focuses on:

- Running FCNV3 on the Nano5 HPC system in Taiwan  
- Providing reproducible environment setup procedures  
- Supporting **both Conda-based and uv-based** environment builds  
- Compiling CUDA-dependent extensions and installing required dependencies  
- Executing FCNV3 inference workflows on Nano5  

---

## Getting Started

Two setup guides are provided. Please choose **one** of the following methods:

### 1. Conda-based environment setup

Follow the instructions in:

```text
run_in_nano5_note.md
```

### 2. uv-based environment setup 

Follow the instructions in:

```text
run_in_nano5_with_uv.md
```