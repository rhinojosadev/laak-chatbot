import os
from flask import Flask, request, jsonify
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from documents.util import UtilSetDocuments, UtilGetContextDocument
from flask_cors import CORS, cross_origin

import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "http://frontend:3000"}})


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"response": "hello from laak"})


@app.route("/api/v1/dbget", methods=["POST"]) 
def db_get():
    try:
        data = request.json
        pregunta = data.get("pregunta", "")
        contexto = UtilGetContextDocument(query=pregunta, db_path='documents/chroma_context_db').get_document()
        return jsonify({"response": contexto})
    except Exception as e:
        return jsonify({"response": "There was an error init"})


@app.route("/api/v1/dbinit", methods=["POST"]) 
def db_init():
    try:
        UtilSetDocuments(file_path='documents/files', db_path='documents/chroma_context_db')
        return jsonify({"response": "Done"})
    except Exception as e:
        return jsonify({"response": "There was an error init"})


@app.route("/api/v1/query", methods=["POST"])
@cross_origin()
def query_docs():
    try:
        data = request.json
        pregunta = data.get("pregunta", "")

        contexto = UtilGetContextDocument(query=pregunta, db_path='documents/chroma_context_db').get_document()
        
        template = """Use the following pieces of context to answer the question at the end. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer, 
                    answer in spanish.\n\n{context}\n\nQuestion: {pregunta}\nHelpful Answer:"""

        prompt = ChatPromptTemplate.from_template(template)

        llm = OllamaLLM(base_url="http://ollama:11434", model="llama3.2:3b")

        chain = prompt | llm

        respuesta = chain.invoke({"pregunta": pregunta,"context": contexto})
       
        return jsonify({"response": respuesta})
    except Exception as e:
        logging.error(f"{e}")
        return e


# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)