import chromadb
from chromadb.utils import embedding_functions


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