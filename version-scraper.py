#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
import requests


if __name__ == "__main__":

    url = "https://esxi-patches.v-front.de/ESXi-6.7.0.html"
    response = requests.get(url).content
    versions = []

    soup = BeautifulSoup(response, "html.parser")
    links = soup.find_all("a", text=True)

    for link in links:
        
        if re.match("ESXi-6.7.[1-20]-[0-9]{11}-standard", link.text):
            versions.append(link.text)
            
    print(versions[0])
