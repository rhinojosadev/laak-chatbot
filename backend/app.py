import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from documents.util import UtilSetDocuments, UtilGetContextDocument
from flask_cors import CORS, cross_origin

import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('flask_cors').level = logging.DEBUG

# Cargar variables de entorno
load_dotenv()

MODEL = os.getenv('MODEL')

OLLAMA_BASE_URL = os.getenv('LLAMA_BASE_URL')
OLLAMA_MODEL = os.getenv('LLAMA_MODEL')

if MODEL == 'qwen':
    OLLAMA_BASE_URL= os.getenv('QWEN_BASE_URL')
    OLLAMA_MODEL= os.getenv('QWEN_MODEL')

DB_PATH = os.getenv('DB_PATH')
FILES_PATH = os.getenv('FILES_PATH')

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
        contexto = UtilGetContextDocument(query=pregunta, db_path=DB_PATH).get_document()
        return jsonify({"response": contexto})
    except Exception as e:
        logging.error(f"dbget {e}")
        return jsonify({"response": "There was an error init"})


@app.route("/api/v1/dbinit", methods=["POST"]) 
def db_init():
    try:
        UtilSetDocuments(file_path=FILES_PATH, db_path=DB_PATH)
        return jsonify({"response": "Done"})
    except Exception as e:
        logging.error(f"dbinit {e}")
        return jsonify({"response": "There was an error init"})


@app.route("/api/v1/query", methods=["POST"])
@cross_origin()
def query_docs():
    try:
        data = request.json
        pregunta = data.get("pregunta", "")

        contexto = UtilGetContextDocument(query=pregunta, db_path=DB_PATH).get_document()
        
        template = """Use the following pieces of context to answer the question at the end. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer, 
                    answer in spanish.\n\n{context}\n\nQuestion: {pregunta}\nHelpful Answer:"""

        prompt = ChatPromptTemplate.from_template(template)

        # llm = OllamaLLM(base_url="http://ollama:11434", model="llama3.2:3b")
        llm = OllamaLLM(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL)

        chain = prompt | llm

        respuesta = chain.invoke({"pregunta": pregunta,"context": contexto})
       
        return jsonify({"response": respuesta})
    except Exception as e:
        logging.error(f"query_docs {e}")
        return jsonify({"response": f"query_docs {e}"})


# Ejecutar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)