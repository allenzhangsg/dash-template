FROM python:3.11-slim

COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-di -r ./requirements.txt

WORKDIR /dash-template
COPY . ./dash-template/

RUN groupadd -r mygroup && useradd -r -g mygroup -d /home/myuser -m myuser
RUN chown -R myuser:mygroup /dash-template /home/myuser
USER myuser

EXPOSE 8000
CMD ["sh", "./run_server.sh"]