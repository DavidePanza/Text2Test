import chromadb
from chromadb.utils import embedding_functions
from .text_processing import text_chunking


def initialize_chromadb(EMBEDDING_MODEL, local_model_path=None):
    """
    Initialize ChromaDB client and embedding function, using a local model path if provided.
    """
    client = chromadb.Client()

    if local_model_path:
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=local_model_path
        )
    else:
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

    return client, embedding_func


def initialize_collection(client, embedding_func, collection_name):
    """
    Initialize a collection in ChromaDB.
    """
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_func,
        metadata={"hnsw:space": "cosine"},
    )

    return collection


def update_collection(
    collection,
    text,
    max_words=200,
    min_words=100,
    overlap_sentences=3,
):
    """
    Update the ChromaDB collection with text chunks.
    Args:
        collection: ChromaDB collection object.
        text (str): The text to be chunked and added.
        max_words (int): Maximum number of words per chunk.
        min_words (int): Minimum number of words per chunk.
        overlap_sentences (int): Number of sentences to overlap between chunks.
    Returns:
        None
    """
    chunks = text_chunking(text, max_words=max_words, min_words=min_words, overlap_sentences=overlap_sentences)
    collection.add(
        documents=chunks,
        ids=[f"chunk_{j:04d}" for j in range(len(chunks))],
        metadatas=[{"chunk_index": j} for j in range(len(chunks))]
    )

