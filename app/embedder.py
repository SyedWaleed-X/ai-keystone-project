# embedder.py

# 1. Import the necessary tools
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
# 2. Load the Document
#    This points to the file we want to process.
loader = TextLoader("H:\AIAce\\ai-keystone-project\data\\knowledge.txt")
documents = loader.load()

# 3. Split the Document into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

print(f"Successfully split the document into {len(chunks)} chunks.")

# 4. Load the Embedding Model
#    The first time you run this, it will download the model (a few hundred MB).
#    After that, it will load it from your local cache.
model = SentenceTransformer('all-MiniLM-L6-v2')

# 5. Create the Vector Embeddings
#    This can take a moment as the model processes each chunk.
#    We need to get just the text content from each LangChain chunk object.
chunk_texts = [chunk.page_content for chunk in chunks]
embeddings = model.encode(chunk_texts)

print(f"Shape of our embeddings matrix: {embeddings.shape}")
# The output will be something like (Number of Chunks, 384)
# 384 is the number of dimensions for this specific model.

print("Time for embedding similarity experiment")

sentences_to_compare = [

"The cat sat on the mat",
"A feline was resting on a rug",
"The rocket launched into space"

]

embedding_experiment = model.encode(sentences_to_compare)

print(f"shape of our experiment embeddings matrix: {embedding_experiment.shape}")

embedding1 = embedding_experiment[0]

embedding2= embedding_experiment[1]

embedding3 = embedding_experiment[2]


distance1vs2 = cosine(embedding1, embedding2)

distances2vs3 = cosine(embedding2, embedding3)


similarity1vs2 = 1 - distance1vs2

similarity2v3 = 1 - distances2vs3

print(f"similairty b/w 1 and 2 {similarity1vs2}")

print(f"similary 2 vs 3 {similarity2v3}")