FROM python:3.7.13-bullseye
ENV LANG C.UTF-8
ENV TZ="Asia/Shanghai"
COPY ./ /home/cookies_pool
WORKDIR /home/cookies_pool
RUN pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
CMD ['python', 'run.py']
