import requests
import feedparser
import re
from os import path
import time
from pathlib import Path

link_regex = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
tor_regex = re.compile(r'https://nyaa.si/download/(\d+).torrent')

base_folder = Path('downloads')

while(True):
    d = feedparser.parse('https://nyaa.si/?page=rss&u=Judas')

    links = []

    for link in link_regex.findall(str(d['entries'])):
        if('nyaa.si/download' in link[0]):
            links.append(link[0])

    for link in links:
        filename = tor_regex.search(link).group(1)

        if not (path.exists(base_folder/(filename+'.torrent')) or path.exists(base_folder/(filename+'.torrent.added')) or path.exists(base_folder/(filename+'.torrent.invalid'))):
            print('Downloading')
            r = requests.get(link, allow_redirects=True)
            open(base_folder/(filename+'.torrent'), 'wb').write(r.content)
        else:
            print('File Already Exists')
    print('checking again in 24 hour')
    time.sleep(86400)
