
import chromadb
import os

from app.embedder import model as embedding_model

from langchain.document_loaders import TextLoader, PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter


CHROMA_DB_PATH = "chroma_data"

COLLECTION_NAME = "knowledge_base"

DATA_Directory = "data/" #folder we'll scan for documents






def populate_vector_store():

    all_chunks = []

    for filename in os.listdir(DATA_Directory):
          
          file_path = os.path.join(DATA_Directory, filename)

          if filename.endswith("pdf"):
                
                print(f"processing PDF {filename}")
                loader = PyPDFLoader(file_path)
                documents = loader.load()
          elif filename.endswith(".txt"):
             print(f"processing txt file {filename}")
             loader = TextLoader(file_path)
             documents = loader.load()
          else:
                continue
          
          text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=100)
          chunks = text_splitter.split_documents(documents)
          
          for chunk in chunks:
                chunk.metadata = {"source": filename}

          all_chunks.extend(chunks)
    if not all_chunks:
          print("no documents found to index, exiting")

          return
            
    print(f"Now creating embeddings for all {len(chunks)} chunks")

    chunk_texts = [chunk.page_content for chunk in all_chunks]

    embeddings = embedding_model.encode(chunk_texts).tolist()
    
    ids = [f"chunk_{i}" for i in range(len(all_chunks))]
    metadatas = [chunk.metadata for chunk in all_chunks]

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    try:
          
          print(f"clearing collection {COLLECTION_NAME}")

          client.delete_collection(name=COLLECTION_NAME)

    except Exception:
          print(f"collection name {COLLECTION_NAME} didnt exist, skipping deletion")

    collection = client.create_collection(COLLECTION_NAME)

    print("Adding documents to the collection")

    collection.add(
          
          ids=ids,
          embeddings=embeddings,
          documents=chunk_texts,
          metadatas=metadatas

    )
    print(f" successfully populated the vector store with {collection.count()} chunks")

    

    

    

if __name__ == "__main__":

        populate_vector_store()



