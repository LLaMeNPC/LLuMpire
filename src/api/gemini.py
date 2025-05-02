from google import genai
from google.genai import types
from api.api import Api, ApiCallResult
import os
import time

api_key = os.environ["GEMINI_KEY"]

class Gemini(Api):

    def request(self, input) -> ApiCallResult:
        max_retries = self.config["max_request_retries"]
        retry_delay = self.config["request_retry_delay"]
        for attempt in range(max_retries - 1):
            try:
                return self._request(input)
            except:
                self.register_retry()
                time.sleep(retry_delay)
        return self._request(input)

    def _request(self, input) -> ApiCallResult:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=input, config=types.GenerateContentConfig(temperature=0.0)
        )

        self.request_num += 1

        return ApiCallResult(
            response.text,
            response.usage_metadata.total_token_count
        )
        

