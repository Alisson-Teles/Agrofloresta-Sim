import requests

# Replace with your OpenRouter API key
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# Define the headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Define the request payload (data)
data = {
    "model": "deepseek/deepseek-chat-v3.1:free",
    "messages": [{"role": "user", "content": "Can you say  hello word ?"}]
}

# Send the POST request to the DeepSeek API
response = requests.post(API_URL, json=data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("API Response:", response.json())
else:
    print("Failed to fetch data from API. Status Code:", response.status_code)