from .embedding_util import generate_embedding

def augment_query(queries: list[str], collection, n_results: int = 10):
    """
    Args:
        queries(list(str)): list of texts to be queried
        collection: reference to the collection to be queried
    Returns:
        a list(str) of query results
    """

    embedding_function = generate_embedding(
        api_key="AIzaSyARLp_PLXXOhjIqf8LStQ9HVNcTiQiuzws"
    )

    embeddings = embedding_function(queries)

    results = collection.query(
        query_embeddings=embeddings,
        n_results=n_results
    )

    return results['documents'][0]



