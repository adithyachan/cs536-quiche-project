import subprocess as sp
import time
import pandas as pd
import argparse

tcp_client_path = "curl"
quiche_client_path = "./client/quiche-client"
quiche_server_url = "172.18.0.3"
http_server_url  = "172.18.0.2"
quiche_server_port = "4433"
http_server_port = "8080"
results_dir = "results/fairness/"

def quiche_client(path="/", connections=1):
    start_time = time.time()
    # Run the specified number of QUIC connections using parallel execution
    sp.run([f"{quiche_client_path}", f"https://{quiche_server_url}:{quiche_server_port}{path}", "--no-verify", "--conns", str(connections)], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def http_client(path="/", connections=1):
    start_time = time.time()
    # Run the specified number of TCP connections using parallel execution
    sp.run([f"{tcp_client_path}", "-k", f"https://{http_server_url}:{http_server_port}{path}", "-o", "/dev/null", "--max-conns", str(connections)], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def measure_throughput(client, bandwidth, connections, output_file):
    # Files to download
    files = ["500KB.txt"]
    data = {file: [] for file in files}
    
    for file in files:
        for _ in range(5):  # Run each test 5 times
            elapsed_time = client(path=f"/{file}", connections=connections)
            throughput_mbps = (500 * 8 * 1000) / elapsed_time / 1_000_000
            data[file].append(throughput_mbps)

    df = pd.DataFrame(data)
    df.to_csv(results_dir + output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare fairness between QUIC and TCP.")
    
    # Add arguments for bandwidth, number of QUIC and TCP connections
    parser.add_argument('--bandwidth', type=int, default=1000, help="Bandwidth in kbps, e.g. 10mbps is 10000")
    parser.add_argument('--quic-conns', type=int, default=1, help="Number of QUIC connections")
    parser.add_argument('--tcp-conns', type=int, default=1, help="Number of TCP connections")
    
    # Parse arguments
    args = parser.parse_args()
    band = 1
    unit = "mbps"
    
    if args.bandwidth >= 1000:
        band = args.bandwidth // 1000
    else:
        band = args.bandwidth
        unit = "kbps"
    
    quic_connections = args.quic_conns
    tcp_connections = args.tcp_conns
    
    # Run the measurements for each connection count
    print(f"Running fairness tests for {band}{unit} bandwidth, {quic_connections} QUIC connections, {tcp_connections} TCP connections")
    
    # Measure QUIC throughput
    measure_throughput(client=quiche_client, bandwidth=args.bandwidth, connections=quic_connections, output_file=f"QUIC_{band}{unit}_conns_{quic_connections}.csv")
    
    # Measure HTTP (TCP) throughput
    measure_throughput(client=http_client, bandwidth=args.bandwidth, connections=tcp_connections, output_file=f"HTTP_{band}{unit}_conns_{tcp_connections}.csv")