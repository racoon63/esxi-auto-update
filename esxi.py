#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
import requests

class Versions(object):

    def __init__(self):
        url       = "https://esxi-patches.v-front.de/ESXi-6.7.0.html"
        response  = requests.get(url).content
        self.soup = BeautifulSoup(response, "html.parser")


    def latest(self):

        versions = self.soup.find_all("a", text=True)
        profiles = []

        for version in versions:
            if re.match("^ESXi-6.7.[0-99]{1,3}-[0-9]{11}s?-standard$", version.text):
                profiles.append(version.text)

        return profiles[0]


    def _get_row_values(self, row):
        
        r = []
        
        row_values = {
            "name": None,
            "version": None,
            "link": None,
            "vendor": None,
            "summary": None,
            "category": None,
            "severity": None,
            "bulletin": None,
            "bg_link": None
        }

        for cell in row("td"):
            r.append(cell.text)
            if cell.a:
                r.append(cell.a.get("href"))

        row_values["name"]     = r[0]
        row_values["version"]  = r[1]
        row_values["link"]     = r[2]
        row_values["vendor"]   = r[3]
        row_values["summary"]  = r[4]
        row_values["category"] = r[5]
        row_values["severity"] = r[6]
        row_values["bulletin"] = r[7]
        row_values["bg_link"]  = r[8]

        return row_values


    def imageprofiles(self):

        tables   = self.soup("table")
        tables   = tables[1:]
        profiles = self.latest()
        versions = []

        for table in tables:
            x = []

            for r in table("tr"):
                if r("td"):
                    x.append(self._get_row_values(r))

            versions.append(x)

        if len(profiles) == len(versions):
            return dict(zip(profiles, versions))
