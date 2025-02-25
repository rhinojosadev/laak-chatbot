#!/bin/bash

# Esperar hasta que Ollama esté disponible
while ! curl -s http://ollama:11434/api/tags > /dev/null; do
    echo "Esperando a que Ollama esté disponible..."
    sleep 2
done

# Descargar el modelo Llama 3
ollama pull meta/llama3

# Iniciar la aplicación Flask
python app.py