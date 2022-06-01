FROM python:3.7.13-bullseye
ENV LANG C.UTF-8
ENV TZ="Asia/Shanghai"
RUN cd /home/cookies_pool
RUN pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
CMD ['python3', 'run.py']
