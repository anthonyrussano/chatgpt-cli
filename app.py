import os
import requests
import json
import openai
from getpass import getpass

VAULT_ADDR = "https://10.32.25.213:8200"

USERNAME = input("Enter your Vault username: ")
PASSWORD = getpass("Enter your Vault Password: ")

url = f"{VAULT_ADDR}/v1/auth/userpass/login/{USERNAME}"
data = {"password": PASSWORD}

response = requests.post(url, json=data, verify=False)  # `verify=False` is equivalent to `-k` in curl

print(f"Login response: {response.text}")

try:
    VAULT_TOKEN = response.json()['auth']['client_token']
except (KeyError, json.JSONDecodeError):
    print("Failed to retrieve Vault token")
    exit(1)


secret_path = 'kv/data/openai'

headers = {
	'X-Vault-Token': VAULT_TOKEN
}

url = f"{VAULT_ADDR}/v1/{secret_path}"

response = requests.get(url, headers=headers, verify=False)

openai_api_key = json.loads(response.text)['data']['data']['api_key']

openai.api_key = openai_api_key

conversation = []

try:
    while True:
        # Get user input
        user_input = input("You: ")
        conversation.append(f"You: {user_input}")

        # Create a prompt using the conversation history
        prompt = "\n".join(conversation)

        # Make API call to OpenAI's GPT engine
        response = openai.ChatCompletion.create(  # Changed this line
            model="gpt-3.5-turbo",  # Model specification
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )

        # Extract and display the model's response
        model_response = response['choices'][0]['message']['content']
        print(f"ChatGPT: {model_response}")

        # Add the model's response to the conversation history
        conversation.append(f"ChatGPT: {model_response}")

except KeyboardInterrupt:
    print("\nConversation ended by user.")