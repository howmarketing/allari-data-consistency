#!/bin/bash


# Initialize conda in your current shell
eval "$(conda shell.bash hook)"

# 1. DIRECT CREATE:
# conda create --name v4 --file conda_requirements.txt

# 1. STAGES CREATE
# Create a new conda environment named 'v4' with Python 3.9.6
conda create --name v4 python=3.9.6

# Activate the 'v4' environment
conda activate v4

# 2. Configure conda channels for package installation
conda config --add channels conda-forge
conda install -n v4 peewee
conda install -n v4 pytest
conda install -n v4 unittest

# 2. Without configure the conda channels for package installation
# conda install -c conda-forge pytest
# conda install -c conda-forge pytest
# conda install -c conda-forge unittest



# 2. OPTIONAL: Install the requirements.txt
# pip install -r requirements.txt
# conda create --name v4 --file conda_requirements.txt
