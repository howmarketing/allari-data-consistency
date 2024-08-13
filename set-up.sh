#!/bin/bash


# Initialize conda in your current shell
eval "$(conda shell.bash hook)"

# 1. DIRECT CREATE:
# conda create --name unit-test --file conda_requirements.txt

# 1. STAGES CREATE
# Create a new conda environment named 'unit-test' with Python 3.9.6
conda create --name unit-test python=3.9.6

# Activate the 'unit-test' environment
conda activate unit-test

# 2. Configure conda channels for package installation
conda config --add channels conda-forge
conda install -n unit-test peewee
conda install -n unit-test pytest
conda install -n unit-test unittest

# 2. Without configure the conda channels for package installation
# conda install -c conda-forge pytest
# conda install -c conda-forge pytest
# conda install -c conda-forge unittest



# 2. OPTIONAL: Install the requirements.txt
# pip install -r requirements.txt
# conda create --name unit-test --file conda_requirements.txt
