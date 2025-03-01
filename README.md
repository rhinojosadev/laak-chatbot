# laak-chatbot

## Instalacion Docker
Windows:
https://docs.docker.com/desktop/setup/install/windows-install/
Otros:
https://docs.docker.com/engine/install/

Despues ejecutra:
docker-compose build

Despues de crear la imagen, ejecutar 
docker-compose up

### Tests
Previamente, se tiene que tener corriendo el modelo OLlama del docker. 
Para configurar, abrir una terminal y situarse en la carpeta de test. 
Luego ahi, ejecutar deepeval set-ollama llama3.2:3b --base-url="http://localhost:11434"