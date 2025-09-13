FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# O comando para iniciar o consumidor
CMD ["python", "consumer.py"]