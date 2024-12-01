FROM cloudflare/quiche:latest

RUN apt-get update
RUN apt-get install -y iproute2 net-tools kmod iperf

RUN mkdir -p /mnt/quiche

COPY quiche-server/entrypoint.sh /mnt
RUN chmod +x /mnt/entrypoint.sh  

WORKDIR /mnt

EXPOSE 4433

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]

# CMD ["./usr/local/bin/quiche-server", "--cert", "/mnt/quiche/certs/cert.crt", "--key", "/mnt/quiche/certs/cert.key", "--root", "/mnt/quiche/files", "--listen", "172.17.0.2:4433"]

