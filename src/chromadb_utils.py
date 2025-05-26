import chromadb
from chromadb.utils import embedding_functions
from text_processing import text_chunking


def initialize_chromadb(EMBEDDING_MODEL):
    """
    Initialize ChromaDB client and embedding function.
    """
    # Create a ephemeral directory for storing the database
    client = chromadb.Client()

    # Initialize an embedding function (using a Sentence Transformer model)
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


def query_collection(collection, query='', nresults=3, sim_th=None):
    """Get relevant text from a collection for a given query"""

    query_result = collection.query(query_texts=query, n_results=nresults)
    docs = query_result.get('documents')[0]

    if sim_th is not None:
        similarities = [1 - d for d in query_result.get("distances")[0]]
        relevant_docs = [d for d, s in zip(docs, similarities) if s >= sim_th]
        return ''.join(relevant_docs)
    return docs