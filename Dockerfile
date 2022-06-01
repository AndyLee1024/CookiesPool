FROM python:3.7.13-bullseye
ENV LANG C.UTF-8
ENV TZ="Asia/Shanghai"
COPY ./entrypoint.sh /home/cookies_pool/entrypoint.sh
RUN chmod +x /home/cookies_pool/entrypoint.sh
CMD ["/home/cookies_pool/entrypoint.sh"]
