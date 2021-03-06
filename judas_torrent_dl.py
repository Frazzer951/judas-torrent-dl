import requests
import feedparser
import re
import os
from os import path
import time
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

link_regex = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
)
tor_regex = re.compile(r"https://nyaa.si/download/(\d+).torrent")

base_folder = Path("downloads")

while True:
    d = feedparser.parse("https://nyaa.si/?page=rss&u=Judas")

    links = []

    for link in link_regex.findall(str(d["entries"])):
        if "nyaa.si/download" in link[0]:
            links.append(link[0])

    for link in links:
        filename = tor_regex.search(link).group(1)

        if not (
            path.exists(base_folder / (filename + ".torrent"))
            or path.exists(base_folder / (filename + ".torrent.added"))
            or path.exists(base_folder / (filename + ".torrent.invalid"))
        ):
            logging.info("Downloading " + link)
            r = requests.get(link, allow_redirects=True)
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)
            open(base_folder / (filename + ".torrent"), "wb").write(r.content)
        # else:
        #    print("File Already Exists")
    logging.info("Checking again in 1 hour")
    time.sleep(3600)
