# ==========================================================
# CRIAR AMBIENTE VIRTUAL E INSTALAR DEPENDÊNCIAS
# ==========================================================
# python -m venv env
# env\Scripts\activate
# pip install -r requirements.txt

import chromadb
import ollama
import os
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# =========================
# CONFIG
# =========================
COLLECTION_NAME = "pdf_collection"
PDF_FOLDER = "pdfs"
MODEL_NAME = "mistral"
EMBED_MODEL = "all-MiniLM-L6-v2"

# =========================
# INIT
# =========================
chromadb_client = chromadb.PersistentClient(path="./chroma_db")
collection = chromadb_client.get_or_create_collection(COLLECTION_NAME)

embedding_model = SentenceTransformer(EMBED_MODEL)

# =========================
# PDF LOAD
# =========================
def load_documents_from_directory(directory):
    documents = []

    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            file_path = os.path.join(directory, file) # Cria o caminho (EX: "pdfs/documento1.pdf")

            reader = PdfReader(file_path) # Lê o PDF usando a biblioteca pypdf

            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

            documents.append({
                "file": file,
                "text": text
            })

    return documents

# =========================
# CHUNKING
# =========================
def create_chunks(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap

    return chunks

# =========================
# EMBEDDINGS
# =========================
def generate_embeddings(text):
    return embedding_model.encode(text).tolist()

# =========================
# INDEX PDFs
# =========================
def build_database():
    count = collection.count()

    if count > 0:
        print(f"Base já carregada ({count} chunks).")
        return

    documents = load_documents_from_directory(PDF_FOLDER)
    print(f"\nLoaded {len(documents)} PDFs\n")

    chunked_documents = []

    for doc in documents:
        chunks = create_chunks(doc["text"])

        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "id": f"{doc['file']}_chunk_{i}",
                "text": chunk
            })

    print(f"Created {len(chunked_documents)} chunks\n")

    for doc in chunked_documents:
        emb = generate_embeddings(doc["text"])

        collection.add(
            ids=[doc["id"]],
            documents=[doc["text"]],
            embeddings=[emb]
        )

    print("Base vetorial criada.\n")

# =========================
# SEARCH
# =========================
def semantic_search(question, n_results=3):
    question_embedding = generate_embeddings(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

    return relevant_chunks

# =========================
# CHAT
# =========================
chat_history = []

def generate_answer(question):
    relevant_chunks = semantic_search(question) # Devolve os chunks mais relevantes para a pergunta

    context = "\n".join(relevant_chunks) # Separo os 3 chunks com uma quebra de linha

    messages = [
        {
            "role": "system",
            "content": "Responde usando o contexto fornecido. Se não souberes, diz que não encontraste nos documentos."
        }
    ]

    # Histórico anterior
    messages.extend(chat_history)

    # Pergunta atual com contexto
    messages.append({ # Adiciona 1 unico elemento à lista
        "role": "user",
        "content": f"Contexto:\n{context}\n\nPergunta: {question}"
    })

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    answer = response["message"]["content"]

    # guardar histórico
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": answer})

    return answer

# =========================
# MAIN LOOP
# =========================
build_database()

print("Chat RAG iniciado.")
print("Escreve 'sair' para terminar.\n")

while True:
    question = input("Tu: ")

    if question.lower() in ["sair", "exit", "quit"]:
        print("Até logo.")
        break

    answer = generate_answer(question)

    print(f"\nBot: {answer}\n")