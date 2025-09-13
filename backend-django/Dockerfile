# 1. Usar uma imagem base oficial do Python
FROM python:3.11-slim

# 2. Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Criar o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Copiar e instalar as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o restante do código da aplicação
COPY . .