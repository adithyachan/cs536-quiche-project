import subprocess as sp
import time
import pandas as pd
import argparse
from concurrent.futures import ThreadPoolExecutor

tcp_client_path = "curl"
quiche_client_path = "./client/quiche-client"
quiche_server_url = "172.18.0.3"
http_server_url  = "172.18.0.2"
quiche_server_port = "4433"
http_server_port = "8080"
results_dir = "results/fairness/"

def quiche_client(file_path="/500KB.txt"):
    start_time = time.time()
    sp.run(
        [quiche_client_path, f"https://{quiche_server_url}:{quiche_server_port}{file_path}", "--no-verify"],
        stdout=sp.DEVNULL,
        stderr=sp.DEVNULL,
    )
    end_time = time.time()
    return end_time - start_time  # Elapsed time

def http_client(file_path="/500KB.txt"):
    start_time = time.time()
    sp.run([tcp_client_path, "-k", "https://" + http_server_url + ":" + http_server_port + file_path, "-o", "/dev/null"], stdout = sp.DEVNULL, stderr = sp.DEVNULL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def run_clients(client_func, file_path, num_clients):
    """Run multiple clients in parallel using threads."""
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [executor.submit(client_func, file_path=file_path) for _ in range(num_clients)]
        return [future.result() for future in futures]

def measure_throughput(client, bandwidth, connections, output_file):
    # Files to download
    file_path = "/500KB.txt"
    file_size_kb = 500
    results = []

    for _ in range(5):  # Run each test 5 times
        elapsed_times = run_clients(client, file_path, connections)
        throughputs = [(file_size_kb * 8 / elapsed_time / 1_000) for elapsed_time in elapsed_times]  # Mbps
        results.extend(throughputs)
        # elapsed_time = client(path=f"/{file}", connections=connections)
        # throughput_mbps = (500 * 8 * 1000) / elapsed_time / 1_000_000
        # data[file].append(throughput_mbps)

    # df = pd.DataFrame(data)
    # df.to_csv(results_dir + output_file, index=False)
    df = pd.DataFrame({f"Throughput (Mbps) for {connections} connections": results})
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