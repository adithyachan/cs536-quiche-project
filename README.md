# CS536 Final Project

- `Makefile` contains commands to build and run various aspects of the system
- `client` is contains client side code intended to be run on the host machine
- `quiche-server` contains everything needed to spin-up a QUICHE file server docker container
- `nginx-server` will contain our HTTP server setup

Currently using the `tc` (Traffic Control) linux utility through a script called "wondershaper" to handle rate-limiting bandwidth of the server to simulate link bandwidth. Ideally, each of the clients run in docker containers which are also bandwidth limited as well but this works for now.

>Note: Do not run the quiche and http servers at the same time as docker will assign one 172.17.0.2 and the other 172.17.0.2. 
> TODO: Need to fix by adding a docker network setup call 

## Quiche Server
Run 
```make build-quiche``` 
to build the docker image 

Run
```make run-quiche```
to run the server (at `172.17.0.2:4433`) and default with 1Mbps bandwidth

Run
```make run-quiche BW=<bandwidth in Kbps>```
to run the server (at `172.17.0.2:4433`) with a specific bandwidth

Ex.
```make run-quiche BW=1000```
runs the server with 1Mbps bandwidth

Run
```make shell-quiche```
to enter the server container and poke around if necessary

Run 
```make kill-quiche```
to kill the server

## HTTP Server
Run 
```make build-http``` 
to build the docker image 

Run
```make run-http```
to run the server (at `172.17.0.2:4433`) and default with 1Mbps bandwidth

Run
```make run-http BW=<bandwidth in Kbps>```
to run the server (at `172.17.0.2:4433`) with a specific bandwidth

Ex.
```make run-http BW=1000```
runs the server with 1Mbps bandwidth

Run
```make shell-http```
to enter the server container and poke around if necessary

Run 
```make kill-http```
to kill the server

## Client

Ideally, supports both the quiche and http client executables. Assuming you are running this on a fresh ubuntu 24.04 EC2 instance.

Run
```sudo apt install python3```
if `python3` is not present on your system

Run
```sudo apt install python3-venv```
if `python3 -m venv` throws an error

Run
```sudo apt install python3-pip```
if `python3 -m pip` throws an error

Run
```python3 -m venv .venv```
to create a virtual environment

Run
```source .venv/bin/activate```
to activate the virtual environment

If this is your first time running `client-runner.py`, then also run 
```python3 -m pip install -r requirements.txt```

Run 
```make run-client```
to run `client-runner.py`. So far it just runs `quiche-client` 10 times for each file and records the file download speed. Need to improve funcationality.

