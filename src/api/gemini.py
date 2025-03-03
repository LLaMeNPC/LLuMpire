from google import genai
import os

api_key = os.environ["GEMINI_KEY"]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)
print(response.usage_metadata.total_token_count)

