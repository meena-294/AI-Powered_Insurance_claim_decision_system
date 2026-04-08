FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask requests

EXPOSE 8000

CMD ["python", "-m",  "server.app"]
