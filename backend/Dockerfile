# Usa una imagen base con Python
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgmp-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app
COPY . /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]