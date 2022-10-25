#!/bin/bash

python -m venv /venv
. /venv/bin/activate
# Ensure pip-tools is installed
python -m pip show pip-tools &> /dev/null
if [ "$?" == "1" ]; then
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install --upgrade 'pip-tools>=6.5.0'
fi

cd docker
pip-compile \
    --generate-hashes \
    --extra-index-url https://download.pytorch.org/whl/cpu/ \
    --extra-index-url https://google-coral.github.io/py-repo/ \
    --output-file _requirements.lock \
    requirements.txt
