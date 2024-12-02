#/bin/bash

ip link add ifb0 type ifb
ip link set dev ifb0 up

if [ -z "$1" ]; then
  BW=1024
else
  BW=$1
fi

echo "Bandwidth value passed: $BW"

# Limit all incoming and outgoing network to 1mbit/s
/bin/bash /mnt/quiche/wondershaper/wondershaper -a eth0 -u $BW -d $BW

ls /usr/local/bin

# Now start your p2p application
/usr/local/bin/quiche-server --cert /mnt/quiche/certs/cert.crt --key /mnt/quiche/certs/cert.key --root /mnt/quiche/files --listen 172.18.0.3:4433
