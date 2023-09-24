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

# Initialize the conversation with a system message
conversation = [
    {"role": "system", "content": "You are a DevOps assistant specialized in Debian Linux environments. Help the user with command line, sysadmin, and DevOps tasks."}
]

try:
    while True:
        # Get user input
        user_input = input("You: ")
        conversation.append({"role": "user", "content": user_input})

        # Make API call to OpenAI's GPT engine using the conversation history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Extract and display the model's response
        model_response = response['choices'][0]['message']['content']
        print(f"ChatGPT: {model_response}")

        # Add the model's response to the conversation history
        conversation.append({"role": "assistant", "content": model_response})

        # Prompt user to save the response to a text file
        save_response = input("Would you like to save this response to a text file? (yes/no): ").strip().lower()
        if save_response == "yes":
            file_name = input("Enter the filename (including path) to save the response: ").strip()
            with open(file_name, "w") as file:
                file.write(model_response)
            print(f"Response saved to {file_name}")

except KeyboardInterrupt:
    print("\nConversation ended by user.")
