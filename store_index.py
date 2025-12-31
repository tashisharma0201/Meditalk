from src.helper import load_pdf_file, text_split
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

# Load env
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

# 1️⃣ Load PDFs
extracted_data = load_pdf_file("Data")
print("Documents loaded:", len(extracted_data))

# 2️⃣ Split to chunks
text_chunks = text_split(extracted_data)
print("Chunks created:", len(text_chunks))

# 3️⃣ Embeddings
embeddings = HuggingFaceEmbeddings(model_name="hf_cache")

# 4️⃣ Pinecone index setup
index_name = "meditalk-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        ),
    )

index = pc.Index(index_name)
print("Index ready:", index_name)

# 5️⃣ Upload vectors
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name,
)

print("Embedding upload completed 🚀")
