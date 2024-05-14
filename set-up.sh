#!/bin/bash

# Initialize conda in your current shell
eval "$(conda shell.bash hook)"

conda create --name ORM_TEST python=3.9.6
conda activate ORM_TEST
conda install --file requirements.txt

conda env config vars set PYTHONPATH="/Users/gabrielariza/Documents/allari/allari-data-consistency"


conda list
