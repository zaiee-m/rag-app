

def augment_query(queries, collection, n_results: int=10):
    """
    Args:
        queries(list(str)): list of texts to be queried
        collection: reference to the collection to be queried
    Returns:
        a list(str) of query results
    """


    results = collection.query(
        query_texts=queries,
        n_results=n_results
    )

    return results['documents'][0]


