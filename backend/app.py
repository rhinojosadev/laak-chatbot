import os
from flask import Flask, request, jsonify
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate

import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


# 📌 1️⃣ Cargar y procesar documentos de distintos formatos
def load_documents(folder):
    documents = []
    print(folder)
    if folder:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file.endswith(".txt"):
                loader = TextLoader(file_path)
            elif file.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(file_path)
            else:
                continue  # Ignorar otros archivos
            
            documents.extend(loader.load())  # Cargar el contenido del archivo
        
        return documents

# 📌 2️⃣ Dividir documentos en fragmentos
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(documents)

# 📌 3️⃣ Crear el vector store
def create_vectorstore(documents):
    if documents:
        vectorstore = Chroma.from_documents(documents, embedding=OllamaEmbeddings())
        return vectorstore.as_retriever()
    
@app.route("/", methods=["GET"])
def hello():
       return jsonify({"response": "hello from laak"})

# 📌 5️⃣ Endpoint para hacer preguntas
@app.route("/query", methods=["POST"])
def query_docs():
    try:
        data = request.json
        pregunta = data.get("pregunta", "")
        print(pregunta)

        contexto=''' ¡Bienvenido a Mi Tiendita! 
            Estamos emocionados de que formes parte de Mi Tiendita, la plataforma que te ayuda a vender fácil y rápido.
            ¿Qué puedes hacer aquí?
            Sube tus productos en minutos.
            Gestiona tus pedidos y clientes desde un solo lugar.
            Recibe pagos seguros y sin complicaciones.
            Personaliza tu tienda para que refleje tu estilo.
            ¡Empecemos!
            Configura tu tienda → Agrega tu logo, descripción y métodos de pago.
            Sube tus productos → Añade fotos, precios y descripciones.
            Comparte tu tienda → Difunde el enlace en redes sociales y empieza a vender.
            ¿Necesitas ayuda? Contáctanos en nuestro centro de soporte.
            ¡Es hora de vender con Mi Tiendita! '''
        
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer, answer in spanish.\n\n{context}\n\nQuestion: {pregunta}\nHelpful Answer:"""

        prompt = ChatPromptTemplate.from_template(template)

        llm = OllamaLLM(base_url="http://localhost:11434", model="llama3.2:3b")

        chain = prompt | llm

        respuesta = chain.invoke({"pregunta": pregunta,"context": contexto})
       
        return jsonify({"response": respuesta})
    except Exception as e:
        logging.error(f"{e}")
        return e


# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)