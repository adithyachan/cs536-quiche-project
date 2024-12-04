# CS536 Final Project - Reproducing "Taking a long look at QUIC" using QUICHE

## Background
[QUIC](https://www.chromium.org/quic/) is a UDP-based transport protocol developed by Google, intended to be a faster and equally reliable alternative to TCP. QUIC has been thoroughly benchmarked in various papers including ["Taking a long look at QUIC" (Kakhki et al., 2017)](https://dl.acm.org/doi/pdf/10.1145/3131365.3131368) and ["Reproducing 'Taking a long look at QUIC'" (Wong et al., 2020)](https://reproducingnetworkresearch.wordpress.com/wp-content/uploads/2020/06/wong_tieu.pdf) where results have shown QUIC to be largely better than or at-par with TCP in most metrics. 

[QUICHE](https://github.com/cloudflare/quiche) is a popular Rust implementation of QUIC with support for many popular clients and servers including NGINX, cURL, and Android. QUICHE is also signficantly easier to build than the Google Chromium implementation of QUIC (which requires building Chromium from scratch and 100 of GB of disk space). QUICHE also has a pre-built docker image which makes it easy to run the server and client in various environments.

## Experimental Setup
- `Makefile` contains commands to build and run various aspects of the system
- `client` is contains client side code intended to be run on the host machine
- `quiche-server` contains everything needed to spin-up a QUICHE file server docker container
- `http-server` contains our HTTP server setup

Currently, we use the `tc` (Traffic Control) linux utility through a script called "wondershaper" to handle rate-limiting bandwidth of the server to simulate link bandwidth. Our client can be run on the host machine.

## Makefile Options

### Quiche Server
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

### HTTP Server
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

### Client

These commands assume you are running this in an Ubuntu 24+ environment. It should work on other MacOS/Linux environments but you may need to use different utilties to handle package management (Homebrew, Yum, etc).

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
to run `download-runner.py` which just runs `quiche-client` and `http-client` 5 times for each file size and records the file download speed for the default (1mbps) link size. The QUICHE and HTTP servers must be running. If you've adjusted the server link size, you can match it with 
```python3 ./client/download-runner.py --bandwidth xxx```

Ex.
```python3 ./client/download-runner.py --bandwidth 1000```
for a 1mbps connection.

By default we sample the following sized files: 5KB, 10KB, 100KB, 200KB, 500KB, 1MB.txt, 10MB

## Generating Test Data
If you are uninterested in running granular operations with the specific client and servers, you may generate test data for 3 different link speeds (10mbps, 100mbps, and 1000mbps) with the command
```make generate-download-data```
This will build both servers then for each link size it will run both servers, run the dowload-runner, and kill both servers. By default we sample the following sized files: 5KB, 10KB, 100KB, 200KB, 500KB, 1MB.txt, 10MB so if you want to test smaller bandwidth speeds you should run the download-runner and remove some of the bigger file sizes. 

TODO: details for fairness, right now just dev notes
Run both servers then ```python3 ./client/fairness-runner.py --quic-conns 3 --tcp-conns 3 --bandwidth 1000```, all 3 paramaters have defaults too

## Results
You can view our results data in the `results` folder. Additionally, the `viz.ipynb` notebook is provided for recreating or modifying our analysis should you choose to do so.

Overall, we found that HTTPS2/TCP beat HTTPS3/QUIC when using the QUICHE server implementation. An interesting anomoly we observed was that the quiche server consistently used only one-third of the given bandwidth, which would largely explain why it failed to keep up with even a simple HTTP server.

Additionally, our methodology, running these experiments through a docker container, simplifies the setup and build process, which we believe gives us a signficant edge over current methodologies using the Chromium QUIC build which takes hours to complete.

## Future Work
We believe there is a lot of room for future work. In particiular, determining the root cause as to why the quiche server perfomed so poorly compared to the Chromium quic server. Additionally, given quiche can integrate directly with cURL and NGINX, these could be used to benchmark performance to provide insight into whether this problem is isolated to the default quiche server or the entire Rust implementation.
