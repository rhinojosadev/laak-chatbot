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

# Instalar Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY requirements.txt ./
COPY . .

# Copiar el script de inicio
COPY start.sh ./
RUN chmod +x start.sh  # Dar permisos de ejecución al script

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto necesario para Flask
EXPOSE 5000

# Comando de inicio
CMD ["./start.sh"]  # Cambiar a ejecutar el script start.sh