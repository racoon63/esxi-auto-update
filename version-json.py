#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
import requests


def get_form(table):
    
    v_template = {}

    for headline in table("th"):
        v_template[headline.text] = None

    return v_template


def get_rows(table):

    rows = []

    for row in table("tr"):
        
        if not row("th"):
            rows.append(row)

    return rows


def get_version(form, row):
    
    cells = row("td")

    form["Name"] = cells[0].text
    form["Version"] = cells[1].text
    form["Vendor"] = cells[2].text
    form["Summary"] = cells[3].text
    form["Category"] = cells[4].text
    form["Severity"] = cells[5].text
    form["Bulletin"] = cells[6].text

    return form


def get_all_profiles():
    
    profiles = []
    versions = soup.find_all("a", text=True)

    for version in versions:
        
        if re.match("ESXi-6.7.*-standard", version.text):
            profiles.append(version.text)

    return profiles


if __name__ == "__main__":

    url = "https://esxi-patches.v-front.de/ESXi-6.7.0.html"
    response = requests.get(url).content
    versions = []

    soup = BeautifulSoup(response, "html.parser")

    tables = soup("table")
    
    for table in tables[2:]:

        form = get_form(tables[1])
        rows = get_rows(tables[1])

        for row in rows:
            versions.append(get_version(form, row))

    print(versions)