FROM python:3.8.10

RUN apt-get update

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /src
COPY src/ .

RUN mkdir -p /logs/tasks
RUN mkdir -p /logs/server
RUN mkdir -p /uploads

RUN chmod +x runserver.sh
RUN chmod +x runworker.sh

CMD ["./runserver.sh"]