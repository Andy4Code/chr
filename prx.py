import time
import requests
from concurrent.futures import ThreadPoolExecutor
from src.proxy import workingProxy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def chprx():
    proxy = workingProxy()  # Change proxy
    proxies = {"http": "http://" + proxy}  # Update proxies dictionary
    return proxies
def twitter(email, proxy):
    proxies = chprx()
    url = "https://api.twitter.com/i/users/email_available.json?email=" + email
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        'Host': "api.twitter.com",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    backoff = 1  # Initial backoff time
    while True:
        try:
            # print(f"{bcolors.OKCYAN} iteration started {bcolors.ENDC}")
            response = requests.get(url, headers=headers, proxies=proxies)
            # print(f"{bcolors.OKCYAN} pass request with proxy {proxies} & status code = {response.status_code} {bcolors.ENDC}")
            if response.status_code == 429:  # If rate limited, change proxy and retry
                #New proxy then  new request
                # print(f"{bcolors.OKCYAN}Rate limited, waiting for {backoff} seconds before retrying{bcolors.ENDC}")
                # time.sleep(backoff)  # Wait for backoff time
                # backoff *= 2  # Exponentially increase backoff time
                proxies = chprx()
                # print(f"{bcolors.OKCYAN}Rate limited, changing proxy to {proxies} {bcolors.ENDC}")
                response = requests.get(url, headers=headers, proxies=proxies)
                # print(f"{bcolors.OKCYAN}[after change] PASS request with proxy {proxies} & status code = {response.status_code} {bcolors.ENDC}")
                # time.sleep(5)
                continue
            # proxy = workingProxy()  # Change proxy
            # proxies = {"http": "http://" + proxy}  # Update proxies dictionary
            # print(f"{bcolors.OKCYAN}Proxy change to : {proxy} {bcolors.ENDC}")
            response.raise_for_status()
            data = response.json()
            if not data.get('valid', False):
                with open("twitter-linked.txt", "a") as file:
                    file.write(email + "\n")
                print(f"{proxies} {bcolors.OKGREEN}{email} {bcolors.ENDC}")
            else:
                with open("not-linked.txt", "a") as file:
                    file.write(email + "\n")
                print(f"{proxies} {bcolors.WARNING}{email} {bcolors.ENDC}")
            # print(f"{bcolors.OKCYAN} iteration ended {bcolors.ENDC}")
            break  # Break out of the loop if request successful
        except requests.exceptions.RequestException as e:
            print(f"{bcolors.FAIL}Error occurred for {email} with proxy {proxies}: {e}{bcolors.ENDC}")
    proxies = chprx()
    # print(f"{bcolors.OKCYAN} changed proxy to {proxies} and sleep {bcolors.ENDC}")
    # time.sleep(15)

def process_emails(emails):
    with ThreadPoolExecutor(max_workers=1) as executor:
        proxy = chprx()  # Get where stop proxy
        executor.map(lambda email: twitter(email, proxy), emails)

if __name__ == '__main__':
    filename = "emails.txt"  # Change this to your input filename
    with open(filename) as f:
        emails = f.readlines()

    process_emails(emails)
