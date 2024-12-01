FROM nginx
COPY nginx-server/files /usr/share/nginx/html

RUN apt-get update
RUN apt-get install -y iproute2 net-tools kmod iperf

RUN mkdir /mnt/nginx

COPY nginx-server/entrypoint.sh /mnt
RUN chmod +x /mnt/entrypoint.sh

EXPOSE 4433


ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
