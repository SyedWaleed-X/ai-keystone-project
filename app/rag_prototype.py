import chromadb

from . ai_handler import get_llm_completion

from . embedder import model as embedding_model


CHROMA_DB_PATH = "chroma_data"

collection_name = "knowledge_base"

PROMPT_fr = """Answer based only on this context, otherwise say "idk bro"

the context is {context}

--
the question is {question}
---
and give your short opinion on the subject/provided context, just a short para/more info to add, anything.
"""

class RAG_Pipeline:

    def __init__(self):

        self.embedding_model = embedding_model
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = client.get_or_create_collection(name=collection_name)

    def _retrieve_context(self, query:str, n_results: int = 1):

        query_embedding = self.embedding_model.encode([query])

        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )

        context = "\n\n--\n\n".join(results['documents'][0])
        source_documents = results['documents'][0]

        return context, source_documents
    
    def _generate_response(self, query:str, context:str):

        prompt = PROMPT_fr.format(context=context, question=query)

        response = get_llm_completion(prompt)

        return response
    
    def ask(self, query: str):

        context, sources = self._retrieve_context(query)

        answer = self._generate_response(query, context)

        return {"answer" : answer, "sources" : sources}




if __name__ == "__main__":
 

    rag_pipeline = RAG_Pipeline()

    answer1 = rag_pipeline.ask("What is a banana like? and its ancestors?")

    print(answer1)







