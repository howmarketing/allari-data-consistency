#!/bin/bash

# Initialize conda in your current shell
conda create --name v4 python=3.9.6
conda activate v4
pip install -r requirements.txt