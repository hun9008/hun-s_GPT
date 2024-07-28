FROM --platform=linux/amd64 python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ollama
RUN ollama run internlm2:latest

EXPOSE 8002

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
