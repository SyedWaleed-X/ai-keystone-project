from langchain.document_loaders import TextLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def  process_document_and_get_embedding(filepath: str, source_id: str):
    print("reading ur document/file rn!!")

    loader = TextLoader(filepath)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

    chunks = text_splitter.split_documents(documents)




    chunk_texts = [chunk.page_content for chunk in chunks]

    embeddings = model.encode(chunk_texts)

    ids = [f"{source_id}_{i}" for i in range(len(chunks))]

    metadatas = [{'source_id': source_id} for _ in chunks ]

    return ids,embeddings,chunk_texts, metadatas



if __name__ == "__main__":


    fileToProcess = "H:\\AIAce\\daily drills and practice\\day 15\\data\\knowledge.txt"

    ids, embeddings,texts, metas = process_document_and_get_embedding(fileToProcess, "knowledge_v1")


    print("now to verify..")

    print(f"shape of our embedding matrix {embeddings.shape}")

    print(f"sample of the first embedding {embeddings[0][:5]}")


    # 7. --- High-ROI Task: The Similarity Experiment ---
    #    This block of code is for hands-on learning and verification.

    # We need the 'cosine' function from the scipy library to measure distance.


