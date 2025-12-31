from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os

load_dotenv()

from pinecone import Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

app = Flask(__name__)
app.secret_key = "meditalk_secret_key"

# Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = os.getenv("INDEX_NAME")

embeddings = HuggingFaceEmbeddings(model_name="hf_cache")
docsearch = PineconeVectorStore.from_existing_index(
    index_name=INDEX_NAME,
    embedding=embeddings
)
retriever = docsearch.as_retriever()

# Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

system_prompt = (
    "You are a professional medical assistant chatbot. "
    "Answer clearly using retrieved medical encyclopedia context. "
    "NEVER guess if unsure. Say 'I don't know based on my data'. "
    "Keep tone empathetic and safe.\n\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


@app.route("/")
def home():
    if "chat" not in session:
        session["chat"] = []
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("msg")

    if "chat" not in session:
        session["chat"] = []

    response = chain.invoke(user_input)

    session["chat"].append({"sender": "user", "text": user_input})
    session["chat"].append({"sender": "bot", "text": response})
    session.modified = True

    return jsonify({"reply": response})


@app.route("/get_chat")
def get_chat():
    return jsonify(session.get("chat", []))


@app.route("/clear_chat")
def clear_chat():
    session["chat"] = []
    session.modified = True
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)
