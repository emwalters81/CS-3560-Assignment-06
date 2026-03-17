from google import genai
import os

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

uploaded_file = client.files.upload(file = "puppies.jpeg")

response = client.models.generate_content(
    model = "gemini-3-flash-preview",
    contents = ["Describe this image for me", uploaded_file]
)

print(response.text)