# =========================
# RAG LOCAL COM PDFS + CHROMADB PERSISTENTE + OLLAMA
# =========================

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) local com suporte a chat, utilizando:

- PDFs como base de conhecimento
- ChromaDB com persistência local
- Sentence Transformers para embeddings
- Ollama (Mistral) como modelo de linguagem
- Histórico de conversa (chat memory)

---

# 🚀 COMO FUNCIONA

## Fluxo do sistema:

PDFs → Extração de texto → Chunking → Embeddings → ChromaDB (persistente)

Pergunta → Embedding → Pesquisa semântica → Contexto + Histórico → Mistral → Resposta

---

# 📦 TECNOLOGIAS

- Python
- ChromaDB (PersistentClient)
- Sentence Transformers
- Ollama
- Mistral
- PyPDF

---

# ⚙️ INSTALAÇÃO

## 1. Criar ambiente virtual

python -m venv env

---

## 2. Ativar ambiente virtual

Windows:
env\Scripts\activate

---

## 3. Instalar dependências

pip install -r requirements.txt

---

## 4. Instalar modelo Ollama

ollama pull mistral

---

# 📂 ESTRUTURA DO PROJETO

project/
│
├── app.py
├── chroma_db/          # Base de dados vetorial persistente
├── pdfs/               # PDFs de conhecimento
├── Images/             # Prints de conversas
└── README.md

---

# 🧠 FUNCIONAMENTO TÉCNICO

## 1. Indexação dos PDFs

- Lê todos os PDFs da pasta `pdfs/`
- Extrai texto
- Divide em chunks
- Gera embeddings
- Guarda no ChromaDB persistente

---

## 2. Pesquisa Semântica

- A pergunta é convertida em embedding
- O sistema procura os chunks mais relevantes
- Retorna contexto relevante

---

## 3. Geração de Resposta

O modelo Mistral recebe:

- Contexto dos PDFs
- Histórico da conversa
- Pergunta atual

E gera uma resposta baseada nesses dados.

---

## 4. Memória de Chat

O sistema mantém histórico da conversa:

- Permite perguntas de seguimento
- Mantém contexto da interação
- Melhora coerência das respostas

---

## 💾 PERSISTÊNCIA (CHROMADB)

Este projeto utiliza:

chromadb.PersistentClient(path="./chroma_db")

Isto significa:

- Os embeddings ficam guardados no disco
- Não é necessário reprocessar PDFs sempre
- Apenas novos PDFs precisam ser adicionados

---

# ▶️ EXECUTAR PROJETO

python main.py

---

# 💬 EXEMPLO DE UTILIZAÇÃO

Chat RAG iniciado.
Escreve 'sair' para terminar.

Tu: Em que cidade posso encontrar os guarda-chuvas coloridos? 

Bot:  A cidade onde pode ser encontrado os guarda-chuvas coloridos é Aveiro.

Tu: E a que distância fica do Aeroporto do Porto?

Bot:  Não encontrei informações nos documentos sobre a distância entre Águeda e o aeroporto mais próximo (Aeroporto do Porto).

---

# 🖼️ EXEMPLOS

Ver pasta:

![Saída do Sistema](Images/saida.png)

Contém prints de conversas reais com o sistema.

---

⚠️ 
Nota técnica: algumas respostas podem não ser totalmente precisas devido às limitações do pipeline RAG utilizado.

Este comportamento pode ser causado por:
- Divisão de texto em chunks (chunking), que pode separar informação relacionada
- Uso do modelo de embeddings "all-MiniLM-L6-v2", que é leve mas menos preciso em relações semânticas complexas
- Limitações na recuperação dos chunks mais relevantes (top-k retrieval)
- Limitações do modelo LLM (Mistral), que pode não utilizar todo o contexto fornecido

Este é um comportamento esperado em sistemas RAG simplificados e pode ser melhorado com modelos de embeddings mais avançados

---

# 🔧 PROCESSO INTERNO

1. Carrega PDFs
2. Divide texto em chunks
3. Cria embeddings
4. Guarda no ChromaDB
5. Pesquisa por similaridade
6. Junta contexto + histórico
7. Gera resposta com Mistral

---

# ⭐ DIFERENÇAS IMPORTANTES (VS VERSÃO 1)

- Usa ChromaDB persistente (não recria base sempre)
- Inclui chat history
- Sistema mais eficiente
- Melhor experiência de conversa

---

# 🎯 OBJETIVO

Criar um assistente local inteligente capaz de responder perguntas com base em documentos PDF, mantendo contexto de conversa e evitando reprocessamento desnecessário.

---

# 👤 AUTOR

Francisco Guedes