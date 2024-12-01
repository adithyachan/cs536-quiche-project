# CS536 Final Project

- `Makefile` contains commands to build and run various aspects of the system
- `client` is contains client side code intended to be run on the host machine
- `quiche-server` contains everything needed to spin-up a QUICHE file server docker container
- `nginx-server` will contain our HTTP server setup

Currently using the `tc` (Traffic Control) linux utility to handle rate-limiting bandwidth of the server to simulate link bandwidth. Ideally, each of the clients runs in docker containers which are also bandwidth limited as well but this works for now.

## Quiche Server
Run 
```make quiche-server``` 
to build the docker image and run the server (at `172.17.0.2:4433`)

Run
```make shell-quiche```
to enter the server container and poke around if necessary

Run 
```make kill-quiche```
to kill the server

## HTTP Server (TODO)
Planning to use nginx for a containerized tcp/http server. Have gotten started on the dockerfile for this.

## Client

Ideally, supports both the quiche and http client executables.

Run
```python -m .venv venv```
to create a virtual environment

Run
```source .venv/bin/activate```
to activate the virtual environment

If this is your first time running `client-runner.py`, then also run 
```pip install -r requirements.txt```

Run 
```make run-client```
to run `client-runner.py`. So far it just runs `quiche-client` 10 times for each file and records the file download speed. Need to improve funcationality.

