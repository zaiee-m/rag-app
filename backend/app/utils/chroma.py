import chromadb
import chromadb.utils.embedding_functions as embedding_functions



def _get_client(chroma_path: str):
    return chromadb.PersistentClient(chroma_path)

def get_client(
        gen_api_key:str, 
        collection_name:str,
        chroma_path:str,
        embedding_model:str="models/text-embedding-004"
    ):
    """
        Args:
            gen_api_key(str): the api_key to use for the embedding function
            collection_name(str): collection to be opened to created
            embedding_model(str, Optional): the default model is models/text-embedding-004
        Returns:
            reference to the opened vector_store collection client
    """

    google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=gen_api_key,
        model_name=embedding_model
    )

    return _get_client(chroma_path).get_or_create_collection(
        embedding_function=google_ef,
        name=collection_name
    )

def remove_collection(
        collection_name:str,
        chroma_path:str
    ) -> None:

    """
        Args:
            collection_name(str): name of the collection to be removed from the vector store
        Returns:
            None
    """

    # Delete the collection if it exists
    try:
        _get_client(chroma_path).delete_collection(name=collection_name)
    except chromadb.errors.NotFoundError:
        pass