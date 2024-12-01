import subprocess as sp
import time
import pandas as pd

quiche_client = "./client/quiche-client"
quiche_server_url = "172.17.0.2"
server_port = "4433"
results_dir = "results/"

def run_quiche_client(path="/"):
    start_time = time.time()
    sp.run([quiche_client, "http://" + quiche_server_url + ":" + server_port + path, "--no-verify"]) 
    end_time = time.time()
    print(path, "(QUICHE):", end_time - start_time)
    return end_time - start_time

def run_tcp_client(path="/"):
    start_time = time.time()
    # TODO: Handle TCP client call, use curl or maybe requests libarary
    sp.run()
    end_time = time.time()
    print("Time (TCP):", end_time - start_time)
    return end_time - start_time

def measure_download_speeds(client=run_quiche_client, output_file="out.csv"):
    files = ["5KB.txt", "10KB.txt", "100KB.txt", "200KB.txt", "500KB.txt", "1MB.txt", "10MB.txt"]

    data = {file: [] for file in files}
    
    for file in files:
        for _ in range(10):
            data[file].append(client("/" + file))

    df = pd.DataFrame(data)
    df.to_csv(results_dir + output_file, index=False)


if __name__ == "__main__":
    measure_download_speeds(output_file="10mbps_QUICHE.csv")
