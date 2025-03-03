from google import genai
from api import api, api_call_result
import os

api_key = os.environ["GEMINI_KEY"]

class gemini(api):

    def request(self, input) -> api_call_result:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=input
        )

        return api_call_result(
            response.text,
            response.usage_metadata.total_token_count
        )
        

api = gemini()
api.request("How has your day been?").print()
