from google import genai
from api.api import Api, ApiCallResult
import os

api_key = os.environ["GEMINI_KEY"]

class Gemini(Api):

    def request(self, input) -> ApiCallResult:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=input
        )

        return ApiCallResult(
            response.text,
            response.usage_metadata.total_token_count
        )
        

