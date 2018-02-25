FROM python:3

WORKDIR /app

COPY image-scraper.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD [ "python", "image-scraper.py" ]
