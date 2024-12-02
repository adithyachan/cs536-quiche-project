import subprocess as sp
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Clients and server setup
tcp_client = "curl"
quiche_client_path = "./client/quiche-client"
server_url = "172.17.0.2"
server_port = "4433"
results_dir = "results/"
file_sizes = {"5KB.txt": 5 * 8, "10KB.txt": 10 * 8, "100KB.txt": 100 * 8, 
              "200KB.txt": 200 * 8, "500KB.txt": 500 * 8, "1MB.txt": 1024 * 8, 
              "10MB.txt": 10240 * 8}  # Sizes in kilobits

def download(client_bin, protocol, path="/"):
    start_time = time.time()
    sp.run([client_bin, "https://" + server_url + ":" + server_port + path, 
            "--no-verify", "-o", "/dev/null"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    end_time = time.time()
    duration = end_time - start_time
    file_size = file_sizes[path.lstrip("/")]
    throughput = file_size / duration  # Throughput in kbps
    print(f"{protocol} {path}: {throughput:.2f} kbps")
    return throughput

def measure_fairness(bandwidth, quic_conns, tcp_conns, file="1MB.txt"):
    data = []
    with ThreadPoolExecutor(max_workers=quic_conns + tcp_conns) as executor:
        # Schedule QUICHE downloads
        for _ in range(quic_conns):
            data.append(executor.submit(download, quiche_client_path, "QUICHE", "/" + file))
        # Schedule TCP downloads
        for _ in range(tcp_conns):
            data.append(executor.submit(download, tcp_client, "TCP", "/" + file))
    # Collect results
    throughputs = [result.result() for result in data]
    return throughputs

def simulate_conditions():
    scenarios = [
        {"bandwidth": 10, "quic_conns": 2, "tcp_conns": 2},
        {"bandwidth": 20, "quic_conns": 3, "tcp_conns": 3},
        # Add more scenarios as needed
    ]
    for scenario in scenarios:
        print(f"Simulating: {scenario}")
        throughputs = measure_fairness(
            bandwidth=scenario["bandwidth"],
            quic_conns=scenario["quic_conns"],
            tcp_conns=scenario["tcp_conns"],
            file="1MB.txt",
        )
        print(f"Results: {throughputs}")

if __name__ == "__main__":
    simulate_conditions()
