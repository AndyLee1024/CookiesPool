FROM python:3.7.13-bullseye
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install libgl1 -y
ENV LANG C.UTF-8
ENV TZ="Asia/Shanghai"
COPY ./entrypoint.sh /entrypoint_run.sh
RUN chmod +x /entrypoint_run.sh
CMD ["/entrypoint_run.sh"]
