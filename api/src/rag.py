import httpx
import numpy as np

from endpoints import Endpoints


def cosine_similarity_vectorized(
    query_embedding: np.ndarray, stored_embeddings: np.ndarray
) -> np.ndarray:
    """
    Calculates cosine similarity between a query vector and a matrix of stored vectors.

    Args:
        query_embedding: A 1D NumPy array representing the query vector.
        stored_embeddings: A 2D NumPy array where each row is a stored embedding vector.

    Returns:
        A 1D NumPy array of cosine similarity scores.
    """
    dot_product = np.dot(stored_embeddings, query_embedding)

    norm_query = np.linalg.norm(query_embedding)
    norm_stored = np.linalg.norm(stored_embeddings, axis=1)

    zero_norm_mask = (norm_query == 0) | (norm_stored == 0)
    similarities = np.zeros_like(dot_product, dtype=float)

    valid_mask = ~zero_norm_mask
    if np.any(valid_mask):
        denominator = norm_stored[valid_mask] * norm_query
        denominator[denominator == 0] = 1e-9
        similarities[valid_mask] = dot_product[valid_mask] / denominator

    # Ensure similarities for zero-norm vectors are explicitly 0.0
    similarities[zero_norm_mask] = 0.0

    return similarities


async def get_embeddings(text: str) -> dict[str, list[float]]:
    async with httpx.AsyncClient() as client:
        embedding = await client.post(
            Endpoints.EMBEDDINGS,
            timeout=10,
            headers={"Content-Type": "application/json"},
            json={
                "model": "text-embedding-nomic-embed-text-v1.5",
                "input": text,
                "stream": False,
            },
        )

        return {text: embedding.json()["data"]["embedding"]}


async def find_most_similar(
    session_hash: str,
    query_text: str,
    vector_db: dict[str, list[dict[str, list[float]]]],
    top_n: int = 1,
) -> list[tuple[str, float]]:
    """
    Performs vector similarity search within a session

    Args:
        session_hash: The hash of the session to search within.
        query_text: The user's input text.
        vector_db: vector database.
        top_n: The number of most similar items to return.

    Returns:
        A list of tuples, where each tuple contains:
        (text_chunk, similarity_score, original_embedding_vector_as_list)
    """
    if session_hash not in vector_db:
        print(f"Session {session_hash} not found.")
        return []

    session_embeddings = vector_db[session_hash]
    if not session_embeddings:
        print(f"No embeddings found for session {session_hash}.")
        return []

    query_embeddings = await get_embeddings(query_text)
    if not query_embeddings:
        print("Could not generate embedding for query text.")
        return []

    query_embedding_np = np.array(list(query_embeddings.values())[0], dtype=np.float32)

    text_chunks = []
    stored_embeddings_list = []

    for embedding_map in session_embeddings:
        for text_chunk, stored_embedding in embedding_map.items():
            text_chunks.append(text_chunk)
            stored_embeddings_list.append(stored_embedding)

    if not text_chunks:  # No valid embeddings found in the session
        print(f"No valid embeddings to compare against in session {session_hash}.")
        return []

    stored_embeddings_np = np.array(stored_embeddings_list, dtype=np.float32)

    similarity_scores = cosine_similarity_vectorized(
        query_embedding_np, stored_embeddings_np
    )

    results_with_scores = []
    for i in range(len(similarity_scores)):
        results_with_scores.append((similarity_scores[i], text_chunks[i]))

    results_with_scores.sort(key=lambda item: item[0], reverse=True)

    top_results = [(text, score) for score, text in results_with_scores[:top_n]]

    return top_results
