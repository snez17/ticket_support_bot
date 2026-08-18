import json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from llama_index.llms.ollama import Ollama

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("storage/index.faiss")
with open("storage/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

llm = Ollama(model="qwen2.5:3b", temperature=0.1)

def classify(text):
    if any(w in text.lower() for w in ['деньги', 'оплата', 'списали', 'платёж']):
        return 'ESCALATE'
    if any(w in text.lower() for w in ['пароль', 'вход', 'логин']):
        return 'AUTO'
    return 'ESCALATE'  # Неизвестное → оператору

def ask(question):
    if classify(question) == 'ESCALATE':
        return "ЭСКАЛАЦИЯ", 0.0
    
    q_emb = model.encode([question], normalize_embeddings=True).astype("float32")
    distances, indices = index.search(q_emb, 3)
    
    if distances[0][0] > 1.5:  # Порог уверенности
        return "ЭСКАЛАЦИЯ", 0.0
    
    context = "\n\n".join([chunks[i] for i in indices[0]])
    prompt = f"Контекст:\n{context}\n\nВопрос: {question}\nОтвет:"
    
    try:
        response = llm.complete(prompt)
        return str(response).strip(), 1.0
    except:
        return "ЭСКАЛАЦИЯ", 0.0