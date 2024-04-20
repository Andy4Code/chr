# -*- coding: utf-8 -*-
# sourced from landoncrabtree on github

"""
This code is licensed under QPL-1.0.
You CAN:
- Distribute
- Modify
You CANNOT:
- Commercial Use
You MUST:
- Include copyright
- Include license
- Disclose source
Source code can be found here:
https://git.landon.pw/r/social-checker
"""

# importing the necessary packages
from itertools import cycle
import requests

# opens the proxy list file and reads it
with open("proxylist.txt", "r+") as f:
    # removes the new line character from the end of each proxy
    proxies = [x.strip() for x in f.readlines()]
    # creates a cycle object so we can iterate through the list indefinitely
proxy_pool = cycle(proxies)

# function to obtain a working proxy
def workingProxy():
    proxy = next(proxy_pool)
    try:
        # attempts to make a request to the ipinfo.io website
        requests.get("http://ipinfo.io/json", proxies={"http": "http://"+proxy}, timeout=5)
        # returns the proxy if it works
        return proxy
    # an exception is thrown if proxy doesn't work
    except Exception as e:
        return workingProxy()
