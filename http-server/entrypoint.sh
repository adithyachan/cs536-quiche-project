#/bin/bash

ip link add ifb0 type ifb
ip link set dev ifb0 up

if [ -z "$1" ]; then
  BW=1024
else
  BW=$1
fi

# Limit all incoming and outgoing network to 1mbit/s
/bin/bash /mnt/wondershaper/wondershaper -a eth0 -u $BW -d $BW

cd /mnt/http-server
# Now start your p2p application
python3 http-server.py
