FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY bot bot/.
COPY scrapers scrapers/.
COPY database_tools database_tools/.

CMD python -u main.py