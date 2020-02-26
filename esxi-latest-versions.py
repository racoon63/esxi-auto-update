#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
import requests


if __name__ == "__main__":

    url      = "https://esxi-patches.v-front.de/ESXi-6.7.0.html"
    response = requests.get(url).content
    soup     = BeautifulSoup(response, "html.parser")
    versions = soup.find_all("a", text=True)
    profiles = []

    for version in versions:

        if re.match("^ESXi-6.7.[0-99]{1,3}-[0-9]{11}s?-standard$", version.text):
            profiles.append(version.text)

    print(profiles[0])
