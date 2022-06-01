FROM python:3.7.13-bullseye
ENV LANG C.UTF-8
ENV TZ="Asia/Shanghai"
COPY ./ /home/cookies_pool
WORKDIR /home/cookies_pool
CMD ["/home/cookies_pool/entrypoint.sh"]
