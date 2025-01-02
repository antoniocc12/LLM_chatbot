FROM python:3.8.10

RUN apt-get update

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR src/
COPY . .

CMD ["python", "scripts/evaluate.py"]