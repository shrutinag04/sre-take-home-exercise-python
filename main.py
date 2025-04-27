import yaml
import requests
import time
from collections import defaultdict
import threading

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint, result_dict):
    url = endpoint['url']
    method = endpoint.get('method','GET')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        response = requests.request(method, url, headers=headers, json=body)
        #print(f"Response for {url}: {response.status_code}, Time: {response.elapsed.total_seconds()}s")
        if 200 <= response.status_code < 300 and (response.elapsed.total_seconds() * 1000) <= 500:
            result_dict[url]= "UP"
        else:
            result_dict[url]= "DOWN"
    except requests.RequestException :
        #print(f"Request failed for {url}: {e}")
        result_dict[url]= "DOWN"


# Function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    # start time
    start_time = time.time()

    while True:
        result_dict = {}

        # thread for each endpoint check
        threads = []
        for endpoint in config:
            thread = threading.Thread(target=check_health, args=(endpoint, result_dict))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Process the results of all endpoints
        for url, result in result_dict.items():
            domain = url.split("//")[-1].split("/")[0].split(":")[0]
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log availability every 15 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time >= 15:
            for domain, stats in domain_stats.items():
                availability = round(100 * stats["up"] / stats["total"])
                print(f"{domain} has {availability}% availability percentage")
            print("---")
            start_time = time.time()
            domain_stats.clear()  

        time.sleep(1)  

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")