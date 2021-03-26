FROM python:3.8.8-buster
MAINTAINER Talmaza Viktoria

WORKDIR /usr/src/python_web-server
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD python main.py

EXPOSE 80