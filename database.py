from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# setting the environment
DATA_PATH = "data"
CHROMA_PATH = "chroma_db"

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create or get the collection
collection = chroma_client.get_or_create_collection(name="data")

# Load the PDF documents
loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()

# Split the document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)

# Prepare embeddings for the documents using OpenAI's embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # Ensure using model with 384-dimension embeddings

# Prepare documents for ChromaDB
documents = []
metadata = []
ids = []

# Process and store each chunk with its embedding
for i, chunk in enumerate(chunks):
    chunk_text = chunk.page_content
    chunk_embedding = embeddings.embed_query(chunk_text)

    # Add data to the list
    documents.append(chunk_text)
    metadata.append(chunk.metadata)
    ids.append(f"ID{i}")

# Upsert data into ChromaDB
collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids,
    embeddings=[embeddings.embed_query(doc) for doc in documents]
)

print(f"Indsat i ChromaDB: {collection.count()}")
