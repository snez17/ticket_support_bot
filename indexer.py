import json, os, numpy as np
from sentence_transformers import SentenceTransformer
import faiss

os.makedirs("storage", exist_ok=True)

with open("data/info.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [text[i:i+500] for i in range(0, len(text), 450)]

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(chunks, normalize_embeddings=True)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "storage/index.faiss")
with open("storage/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print(f"✅ Индекс создан. Чанков: {len(chunks)}")