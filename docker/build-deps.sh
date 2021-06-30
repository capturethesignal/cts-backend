#!/bin/bash

export PYTHON=${PYTHON:-python}
export PIP=${PIP:-pip}
export PIPFILE=${PIPFILE:-requirements.pip}
export SETUP_ENV=${SETUP_ENV:-/pybombs/setup_env.sh}

env

cd ${VOLUME}

source ${SETUP_ENV}

ldconfig

# install any deps
find . -type f -name 'setup.py' | while read f; do
    echo "Installing Python deps"
    cd $(dirname "${f}")
    ${PYTHON} setup.py install
done

if [ -f "${PIPFILE}" ]; then
    echo "Installing Python deps from: ${PIPFILE}"
    ${PIP} install -r "${PIPFILE}"
fi
