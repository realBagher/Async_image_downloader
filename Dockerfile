FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y 

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENTRYPOINT ["python", "src/main.py"]


