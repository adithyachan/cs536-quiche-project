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
results_dir = "results/download_speed/"

def quiche_client(path="/"):
    start_time = time.time()
    sp.run([quiche_client_path, "https://" + quiche_server_url + ":" + quiche_server_port + path, "--no-verify"], stdout = sp.DEVNULL, stderr = sp.DEVNULL) 
    end_time = time.time()
    print(path, "(QUICHE):", end_time - start_time)
    return end_time - start_time

def http_client(path="/"):
    start_time = time.time()
    sp.run([tcp_client_path, "-k", "https://" + http_server_url + ":" + http_server_port + path, "-o", "/dev/null"], stdout = sp.DEVNULL, stderr = sp.DEVNULL)
    end_time = time.time()
    print(path, "(TCP):", end_time - start_time)
    return end_time - start_time

def measure_download_speeds(client=quiche_client, output_file="out.csv"):
    files = ["5KB.txt", "10KB.txt", "100KB.txt", "200KB.txt", "500KB.txt", "1MB.txt", "10MB.txt"]

    data = {file: [] for file in files}
    
    for file in files:
        for _ in range(10):
            data[file].append(client("/" + file))

    df = pd.DataFrame(data)
    df.to_csv(results_dir + output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare download speeds of QUICHE vs HTTP.")
    
    # Add argument for bandwidth (output file name)
    parser.add_argument('--bandwidth', type=int, default=1000, help="Bandwidth in kbps, e.g. 10mbps is 10000")
    
    # Parse arguments
    args = parser.parse_args()
    band = 1
    unit = "mbps"
    if args.bandwidth >= 1000:
        band = args.bandwidth // 1000
    else:
        band = args.bandwidth
        unit = "kbps"
    
    # Run the measurements with the provided bandwidth
    print(f"Running tests for {band}{unit} bandwidth")
    measure_download_speeds(client=quiche_client, output_file=f"{band}{unit}_QUICHE.csv")
    measure_download_speeds(client=http_client, output_file=f"{band}{unit}_HTTP.csv")
