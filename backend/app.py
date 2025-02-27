import os
from flask import Flask, request, jsonify
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Configuración del servidor Fl
# ask
app = Flask(__name__)
# 📂 Carpeta donde están los documentos (PDF, TXT, DOCX)
DOCS_FOLDER = "documents"

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
        vectorstore = Chroma.from_documents(documents, embedding=OpenAIEmbeddings())
        return vectorstore.as_retriever()


# 📌 5️⃣ Endpoint para hacer preguntas
@app.route("/query", methods=["POST"])
def query_docs():
    data = request.json
    query = data.get("query", "")
    
    if not query:
        return jsonify({"error": "La consulta está vacía"}), 400
    
    # 📌 4️⃣ Configurar el modelo Llama 3 con Ollama
    llm = Ollama(model="llama3")

    # Cargar documentos y crear el vector store
    docs = load_documents(DOCS_FOLDER)
    split_docs = split_text(docs)
    retriever = create_vectorstore(split_docs)

    # Crear la cadena de RAG
    # No funciona
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
        
    response = qa_chain.run(query)

    return jsonify({"response": response})

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)