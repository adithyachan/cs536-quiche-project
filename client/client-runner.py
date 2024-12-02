import subprocess as sp
import time
import pandas as pd

tcp_client_path = "curl"
quiche_client_path = "./client/quiche-client"
server_url = "172.17.0.2"
server_port = "4433"
results_dir = "results/"

def quiche_client(path="/"):
    start_time = time.time()
    sp.run([quiche_client_path, "https://" + server_url + ":" + server_port + path, "--no-verify"], stdout = sp.DEVNULL, stderr = sp.DEVNULL) 
    end_time = time.time()
    print(path, "(QUICHE):", end_time - start_time)
    return end_time - start_time

def http_client(path="/"):
    start_time = time.time()
    sp.run([tcp_client_path, "-k", "https://" + server_url + ":" + server_port + path, "-o", "/dev/null"], stdout = sp.DEVNULL, stderr = sp.DEVNULL)
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
    measure_download_speeds(client=quiche_client, output_file="10mbps_Q.csv")
    measure_download_speeds(client=http_client, output_file="10mbps_HTTP.csv")
