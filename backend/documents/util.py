import os

from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_chroma import Chroma

'''
    Este clase guarda los documentos y crea la base de datos 
'''
class UtilSetDocuments:
    def __init__(self, file_path, db_path):
        self.db_path = db_path
        split_documents = UtilSetDocuments.text_split(UtilSetDocuments.read_text(file_path))
        embeddings = UtilSetDocuments.embedding_ollama()
        UtilSetDocuments.create_vector_db(self, docs=split_documents, embeddings=embeddings)


    def read_text(path):
        documents = []
        try:
            if path:
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    if file.endswith(".pdf"):
                        loader = PyPDFLoader(file_path)
                    elif file.endswith(".txt"):
                        loader = UnstructuredLoader(file_path)
                    elif file.endswith(".docx"):
                        loader = UnstructuredWordDocumentLoader(file_path)
                    else:
                        continue  
                    documents.extend(loader.load())  

                return documents
        except Exception as e:
            print(e)

    def text_split(documents):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=100,
                chunk_overlap=20,
                add_start_index=True                                      
            )
            return text_splitter.split_documents(documents)
        except Exception as e:
            print(e)

    def embedding_ollama():
        try:
            return OllamaEmbeddings(base_url="http://localhost:11434", model="llama3.2:3b")
        except Exception as e:
            print(e)

    def create_vector_db(self, docs, embeddings):

        try:
            vector_store = Chroma.from_documents(
                documents=filter_complex_metadata(docs),
                embedding=embeddings,
                persist_directory=self.db_path
            )
            return vector_store
        except Exception as e:
            print(e)

'''
    Este clase obtiene los datos de la base de datos
'''
class UtilGetContextDocument:
    def __init__(self, query, db_path):
        self.db_path = db_path
        embeddings = UtilSetDocuments.embedding_ollama()
        vector_store = Chroma(persist_directory=db_path, embedding_function=embeddings)
        self.retriver = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )
        self.query = query

    def get_document(self):
        retrived_docs = self.retriver.invoke(self.query)
        return "\n\n".join([doc.page_content for doc in retrived_docs])