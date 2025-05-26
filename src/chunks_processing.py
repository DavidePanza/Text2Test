import random


def query_collection(collection, query='', nresults=3, context_multiplier=2, sim_th=None):
    """Get relevant text from a collection for a given query"""

    query_result = collection.query(query_texts=query, n_results=nresults*context_multiplier)
    docs = query_result.get('documents')[0]

    if sim_th is not None:
        similarities = [1 - d for d in query_result.get("distances")[0]]
        relevant_docs = [d for d, s in zip(docs, similarities) if s >= sim_th]
        return ''.join(relevant_docs)
    return docs


def get_chapter_context(chapters, chapter_number, n_questions):
    chapter = chapters[chapter_number]
    if chapter is None:
        raise ValueError(f"Chapter {chapter_number} not found in the chapters list.")
    if 'chunks' not in chapter:
        raise ValueError(f"Chapter {chapter_number} does not contain 'text' key.")
    
    n_chunks = len(chapter['chunks'])
    if n_chunks == 0:
        raise ValueError(f"Chapter {chapter_number} has no chunks to process.")
    
    chunks_indices = random.sample(range(n_chunks), min(n_questions, n_chunks))
    selected_chunks = [chapter['chunks'][i] for i in chunks_indices]
    return selected_chunks