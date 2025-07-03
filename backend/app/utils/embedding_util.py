from google import genai

class generate_embedding():

    def __init__(self,
            api_key:str,
            model_name:str="models/text-embedding-004"
        ):

        self._api_key = api_key
        self._model = model_name
        self._client = genai.Client(api_key=self._api_key)

    def __call__(self, input : list[str]):
        try:
            return [
                self._client.models.embed_content(
                    model=self._model,
                    contents=text
                ).embeddings[0].values
                for text in input
            ]
        except genai.errors.APIError as e:
            raise e
        