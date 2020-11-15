FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY bot bot/.
COPY scrapers scrapers/.
COPY postgres postgres/.

CMD python -u main.py