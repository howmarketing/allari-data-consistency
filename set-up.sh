#!/bin/bash

# Initialize conda in your current shell
eval "$(conda shell.bash hook)"

conda create --name APP-V3-LAB-V1 python=3.9.6
conda activate APP-V3-LAB-V1
conda install --file requirements.txt

conda env config vars set PYTHONPATH="/Users/gabrielariza/Documents/allari/application/V3"


conda list
