# 🩺 MediTalk – AI-Powered Medical Assistant

MediTalk is a **Generative AI medical assistant** that helps users understand
health conditions, symptoms, first aid, and medical concepts using **trusted medical
encyclopedia data**.  
It supports **text + voice input**, **spoken responses**, and **real-time chat UI**.


## ✨ Feature

- 💬 Real-time chat interface 
- 🎤 Voice input (Speech-to-Text)
- 🔊 Text-to-Speech (bot speaks answers)
- 📚 RAG-based answers using medical PDFs
- 🔍 Semantic search using Pinecone Vector DB
- ⚡ Fast and lightweight UI
- 🧠 Context-aware medical responses


## 🏗️ Tech Stack

**Frontend**
- HTML, CSS, JavaScript

**Backend**
- Flask (Python)
- LangChain
- Sentence Transformers (CPU)
- Pinecone (Vector Database)

**AI / NLP**
- HuggingFace sentence-transformers
- Groq 

## 🚀 How It Works

1. Medical PDFs are loaded and split into chunks
2. Text is converted into embeddings using Sentence Transformers
3. Embeddings are stored in Pinecone
4. User query → relevant chunks retrieved
5. LLM generates a safe, concise response
6. Answer is shown and optionally spoken aloud