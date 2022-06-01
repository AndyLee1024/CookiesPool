#!/bin/bash

cd /home/cookies_pool
pip install -r requirements.txt -i https://pypi.doubanio.com/simple
python run.py

