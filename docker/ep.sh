#!/bin/bash

export SETUP_ENV=${SETUP_ENV:-/pybombs/setup_env.sh}
export PYTHON=${PYTHON:-python}
export PIP=${PIP:-pip}
export PIPFILE=${PIPFILE:-requirements.pip}

export MAIN=${MAIN:-main.sh}
export BOMB=${BOMB:-/bomb}

cd ${BOMB}

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

# main
if [ -f "${MAIN}" ]; then
    echo "Executing: ${MAIN}"
    exec ./${MAIN}
else
    echo "No ${MAIN} found: doing nothing"
fi
