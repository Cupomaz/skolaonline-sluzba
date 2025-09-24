FROM python:3.14.0rc3-alpine3.22

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY ntpd.conf /etc/ntpd.conf

RUN apk update && apk add --no-cache cronie openntpd && \
    pip install -r requirements.txt && \
    chmod +x main.py

COPY crontab /etc/crontabs/root

CMD ["sh", "-c", "ntpd -d -f /etc/ntpd.conf & crond -f -L /dev/stdout"]