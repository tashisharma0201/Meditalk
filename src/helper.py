from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings


# Extract data from PDF directory
def load_pdf_file(path):
    loader = DirectoryLoader(
        path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()
    return documents


# Split extracted documents into chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks


# HuggingFace Embeddings (using your local cache)
embeddings = HuggingFaceEmbeddings(
    model_name="hf_cache"
)
