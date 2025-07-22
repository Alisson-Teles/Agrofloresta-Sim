from google import genai

client = genai.Client(api_key="AIzaSyBJhrCvTi8FGtIQRYCu7DslTq_6g9I8Af4")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)