import requests
import math

# Sample knowledge base
documents = [
    "The Eiffel Tower is located in Paris.",
    "Python is a popular programming language.",
    "The Moon orbits the Earth every 27.3 days.",
    "OpenAI develops powerful AI tools.",
]


# Simple tokenizer and vectorizer
def tokenize(text):
    return text.lower().split()


def vectorize(text, vocab):
    tokens = tokenize(text)
    return [tokens.count(word) for word in vocab]


def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x**2 for x in a))
    norm_b = math.sqrt(sum(y**2 for y in b))
    return dot / (norm_a * norm_b + 1e-8)

def retrieve(query, vocab, doc_vectors, k=2):
    query_vec = vectorize(query, vocab)
    sims = [cosine_sim(query_vec, doc_vec) for doc_vec in doc_vectors]
    top_indices = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:k]
    return [documents[i] for i in top_indices]


# Function to send request to LM Studio's /v1/chat/completions
def query_lm_studio(
    context, question, endpoint="http://127.0.0.1:1234/v1/chat/completions"
):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant using provided context.",
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False,
    }
    response = requests.post(endpoint, json=payload)
    return response.json()["choices"][0]["message"]["content"]


# RAG pipeline
def rag_query(question):
    context = "\n".join(retrieve(question))
    answer = query_lm_studio(context, question)
    print(f"Q: {question}\nA: {answer}")

