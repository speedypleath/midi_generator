#!/bin/bash

bash scripts/clean.sh

# build the project
python3 -m build

# install the module
pip3 install --force-reinstall dist/*.whl