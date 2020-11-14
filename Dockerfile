FROM python:3

ADD judas_torrent_dl.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

RUN mkdir /downloads
VOLUME [ "/downloads" ]

CMD ["python", "-u", "./judas_torrent_dl.py"]