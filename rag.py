import json, numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from llama_index.llms.ollama import Ollama
from datetime import datetime
import os

LOG_FILE = "logs/tickets.log"
os.makedirs("logs", exist_ok=True)

def log_ticket(ticket_id, action, content=""):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%d.%m.%y %H:%M:%S")
        f.write(f"[{time}] #{ticket_id} {action} {content}\n")

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("storage/index.faiss")
with open("storage/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

llm = Ollama(model="qwen2.5:3b", temperature=0.1)

def classify_ticket(text):
    # Категории и риски
    if any(w in text.lower() for w in ['деньги', 'оплата', 'списали', 'платёж', 'возврат']):
        return 'Платежи', 'HIGH'
    elif any(w in text.lower() for w in ['пароль', 'вход', 'логин', 'регистрация']):
        return 'Аккаунт', 'LOW'
    elif any(w in text.lower() for w in ['скидка', 'промокод', 'бонус']):
        return 'Бонусы', 'LOW'
    else:
        return 'UNKNOWN', 'MEDIUM'
    
ticket_counter = 0

def ask(question):
    global ticket_counter
    ticket_counter += 1
    ticket_id = ticket_counter
    
    # Лог: получено сообщение
    log_ticket(ticket_id, "Получено сообщение", f"'{question}'")

    topic, risk = classify_ticket(question)

    # Лог: присвоен риск
    log_ticket(ticket_id, f"Присвоен риск '{risk}'", f"(тема: {topic})")

    if risk == 'HIGH' or topic == 'UNKNOWN':
        return "ЭСКАЛАЦИЯ", 0.0
    
    q_emb = model.encode([question], normalize_embeddings=True).astype("float32")
    distances, indices = index.search(q_emb, 3)
    
    if distances[0][0] > 1.5:  # Порог уверенности
        log_ticket(ticket_id, "Ответ направлен оператору (низкая уверенность)")
        return "ЭСКАЛАЦИЯ", 0.0
    
    context = "\n\n".join([chunks[i] for i in indices[0]])
    prompt = f"Контекст:\n{context}\n\nВопрос: {question}\nОтвет:"
    
    try:
        response = llm.complete(prompt)
        answer = str(response).strip()
        log_ticket(ticket_id, "Отправлен автоответ", f"'{answer}'")
        return answer, 1.0
    except:
        log_ticket(ticket_id, "Ошибка LLM, направлен оператору")
        return "ЭСКАЛАЦИЯ", 0.0