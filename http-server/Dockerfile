FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y iproute2 net-tools kmod iperf python3

RUN mkdir /mnt/http-server
RUN mkdir /mnt/http-server/wondershaper

COPY http-server/entrypoint.sh /mnt
RUN chmod +x /mnt/entrypoint.sh

COPY http-server/http-server.py /mnt/http-server
COPY http-server/mount/certs /mnt/http-server
COPY http-server/mount/files /mnt/http-server
COPY http-server/mount/wondershaper /mnt/wondershaper

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "/mnt/entrypoint.sh"]
