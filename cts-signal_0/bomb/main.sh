#!/bin/bash

source /pybombs/setup_env.sh

ldconfig

sed 's/gitbranch\: master/gitbranch: maint-3.7/g' \
    /root/.pybombs/recipes/gr-recipes/gr-paint.lwr > \
    /root/.pybombs/recipes/gr-recipes/gr-paint37.lwr
pybombs install gr-paint37

make all

python signal.py
