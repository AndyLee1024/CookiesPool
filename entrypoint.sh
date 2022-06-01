#!/bin/bash

# shellcheck disable=SC2164
cd /home/cookies_pool
pip install -r requirements.txt -i https://pypi.doubanio.com/simple
python run.py

