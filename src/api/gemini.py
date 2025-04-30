from google import genai
from api.api import Api, ApiCallResult
import os
import time
from log import log

api_key = os.environ["GEMINI_KEY"]

class Gemini(Api):

    def request(self, input, max_retries=5, retry_delay=2) -> ApiCallResult:
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
            model="gemini-2.0-flash", contents=input
        )

        self.request_num += 1

        return ApiCallResult(
            response.text,
            response.usage_metadata.total_token_count
        )
        

