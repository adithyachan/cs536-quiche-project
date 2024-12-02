# CS536 Final Project

- `Makefile` contains commands to build and run various aspects of the system
- `client` is contains client side code intended to be run on the host machine
- `quiche-server` contains everything needed to spin-up a QUICHE file server docker container
- `http-server` contains our HTTP server setup

Currently using the `tc` (Traffic Control) linux utility through a script called "wondershaper" to handle rate-limiting bandwidth of the server to simulate link bandwidth. Ideally, each of the clients run in docker containers which are also bandwidth limited as well but this works for now.


## Quiche Server
Assigned IP 172.18.0.3
Run 
```make build-quiche``` 
to build the docker image 

Run
```make run-quiche```
to run the server (at `172.18.0.3:4433`) and default with 1Mbps bandwidth

Run
```make run-quiche BW=<bandwidth in Kbps>```
to run the server (at `172.18.0.3:4433`) with a specific bandwidth

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
to run the server (at `172.18.0.2:8080`) and default with 1Mbps bandwidth

Run
```make run-http BW=<bandwidth in Kbps>```
to run the server (at `172.18.0.3:8080`) with a specific bandwidth

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
```python3 ./client/download-runner.py```
to run `download-runner.py` which just runs `quiche-client` and `http-client` 10 times for each file size and records the file download speed for the default (1mbps) link size. The QUICHE and HTTP servers must be running. If you've adjusted the server link size, you can match it with 
```python3 ./client/download-runner.py --bandwidth xxx```

Ex.
```python3 ./client/download-runner.py --bandwidth 1000```
for a 1mbps connection.

## Generating Test Data
If you are uninterested in running granular operations with the specific client and servers, you may generate test data for 5 different link speeds with. This will build both servers then for each link size it will run both servers, run the dowload-runner, and kill both servers. 
```make generate-download-data```