FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY version-scraper.py /app/version-scraper.py

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "version-scraper.py" ]
