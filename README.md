# laak-chatbot



https://github.com/user-attachments/assets/c6d1d297-0ef2-429a-be8e-e8efb8f4fb12




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
