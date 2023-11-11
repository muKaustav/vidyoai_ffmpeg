FROM jrottenberg/ffmpeg:4.4-ubuntu

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . .

ENTRYPOINT []

CMD ["celery", "-A", "worker.celery", "worker", "--loglevel=info", "--concurrency=10", "--uid=nobody"]
