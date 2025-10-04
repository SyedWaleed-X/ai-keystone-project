import chromadb


from app.embedder import process_document_and_get_embedding


CHROMA_DB_PATH = "chroma_data"

COLLECTION_NAME = "knowledge_base"


print("initialize client to save info perma")

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)



def rest_and_populate_vector_store(file_path: str, source_id : str):

    ids, embeddings, text, metadatas = process_document_and_get_embedding(
        filepath=file_path, source_id=source_id
    )

    try:
          
          print(f"clearing collection {COLLECTION_NAME}")
          client.delete_collection(name=COLLECTION_NAME)
    except Exception as e:
          print(f"Collection {COLLECTION_NAME} didn't exist,skipping clear")

    print(f"Accessing collection {COLLECTION_NAME}")

    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection.add(

        ids=ids,
        embeddings=embeddings.tolist(),
        documents=text,
        metadatas=metadatas
    )

    print("successfuly populated the vector store")


if __name__ == "__main__":

        file_to_process = "H:\\AIAce\\ai-keystone-project\\data\\knowledge.txt"

        source_identifier = "knowledge_base_v1"

        rest_and_populate_vector_store(

            file_path=file_to_process,
            source_id=source_identifier
        )

        print("Testing")

        collection = client.get_collection(name=COLLECTION_NAME)

        results = collection.query(

            query_texts="tell me about gintama bro",
            n_results=1
        )

        print("Top result")
        print(results["documents"][0][0])



