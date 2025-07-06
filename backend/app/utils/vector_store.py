from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import chromadb
import asyncio
from itertools import islice
from google import genai
from google.genai import errors
import chromadb.utils.embedding_functions as embedding_functions
from uuid import uuid4


CHUNK_SIZE = 2_000
CHUNK_OVERLAP = 250
BATCH_SIZE = 100
EMBEDDING_MODEL = "models/text-embedding-004"

async def load_vector_store(file_path: str, chroma_path: str, api_key: str, collection_name: str):

    """
        Load a vector store from a specified file path.

        Args:
            file_path (str): The path to the vector store file.
            collection_name (str): The name of the collection to load. Defaults to None.
            chroma_path (str): The path to the Chroma database. Defaults to None.
            api_key (str): API key for authentication, if required. Defaults to None.

        Returns:
            VectorStore: An instance of the loaded vector store.
    """

    # Client for gemini api requests

    try:
        client = genai.Client(api_key=api_key)
    except genai.errors.APIError as e:
        raise e

    try:
        file = open(file_path)
    except OSError as e:
        raise OSError("Could not open file")


    with file:
        document = file.read()


    # Initialize text_splitter to split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents([document])
    print("", end="\n\n\n\n")
    print(len(texts), end="\n\n\n\n")

    google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=api_key,
        model_name=EMBEDDING_MODEL
    )

    # Generate chunks of 100 texts each.
    chunks = (chunk for chunk in _chunk_list(texts, BATCH_SIZE))
    embeddings_generated = []
    flag = 0

    while len(embeddings_generated) < len(texts)/BATCH_SIZE:
        try:
            batch = islice(chunks, 100)

            results_received = await asyncio.gather(
                *[
                    client.aio.models.embed_content(
                        model=EMBEDDING_MODEL,
                        contents=chunk
                    )for chunk in batch
                ],
                return_exceptions=False
            )
            embeddings_generated.extend(results_received)
        except genai.errors.APIError as e:
            print("Frick")
            if e.code == 429:
                if flag == 2:
                    raise e
                flag+=1 # Retries three times if embedding fails
                pass
            else:
                raise e

        await asyncio.sleep(60)

    print(len(embeddings_generated), end="\n\n\n\n")
    # Initialize vector store client
    persistent_client = chromadb.PersistentClient(chroma_path)
    print("client successfully opened", end="\n\n\n\n")

    # Create a new vector store collection if first request from session
    collection = persistent_client.get_or_create_collection(
        embedding_function=google_ef,
        name=collection_name
    )

    # Load chunks into vector store in batches of BATCH_SIZE max
    try:
        for chunk, chunk_embeddings in zip( _chunk_list(texts, BATCH_SIZE), embeddings_generated):
            collection.add(
                documents=chunk,
                embeddings=[
                    embedding.values for embedding in chunk_embeddings.embeddings
                ],
                ids=[
                    str(uuid4()) for _ in range(len(chunk))
                ]
            )

    except ValueError as error:
        raise error
    except chromadb.errors.DuplicateIDError as error:
        raise error

    # Return reference to the collection to be passed to the query utility function
    # Or to be queried
    return collection




def _chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        result = []
        for text in lst[i:i+chunk_size]:
            result.append(text.page_content)
        yield result
