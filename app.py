import os
import requests
import json
import openai
from getpass import getpass
from datetime import datetime
import re

VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://10.32.25.213:8200")

def authenticate_with_vault(username, password):
    url = f"{VAULT_ADDR}/v1/auth/userpass/login/{username}"
    data = {"password": password}
    response = requests.post(url, json=data)
    try:
        return response.json()['auth']['client_token']
    except (KeyError, json.JSONDecodeError):
        print("Failed to retrieve Vault token")
        exit(1)

def get_openai_api_key(vault_token):
    secret_path = 'kv/data/openai'
    headers = {'X-Vault-Token': vault_token}
    url = f"{VAULT_ADDR}/v1/{secret_path}"
    response = requests.get(url, headers=headers)
    return json.loads(response.text)['data']['data']['api_key']

def generate_timestamped_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"responses/response_{timestamp}.md"

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def chat_with_openai():
    conversation = [
        {
            "role": "system",
            "content": (
                ""
            )
        }
    ]


    ensure_directory_exists("responses")

    try:
        while True:
            user_input = input("You: ")
            conversation.append({"role": "user", "content": user_input})

            response = openai.ChatCompletion.create(model="gpt-4", messages=conversation)
            model_response = response['choices'][0]['message']['content']
            print(" ")
            print(f"ChatGPT: {model_response}")
            print(" ")
            conversation.append({"role": "assistant", "content": model_response})

            response_parts = model_response.split(":", 1)
            if len(response_parts) != 2:
                file_name = generate_timestamped_filename()
                content_to_save = model_response
            else:
                suggested_filename, content_to_save = response_parts
                file_name = f"responses/{suggested_filename.strip()}"

            with open(file_name, "w") as file:
                file.write(content_to_save.strip())

    except KeyboardInterrupt:
        print("\nConversation ended by user.")

if __name__ == "__main__":
    USERNAME = input("Enter your Vault username: ")
    PASSWORD = getpass("Enter your Vault Password: ")
    VAULT_TOKEN = authenticate_with_vault(USERNAME, PASSWORD)
    openai_api_key = get_openai_api_key(VAULT_TOKEN)
    openai.api_key = openai_api_key
    chat_with_openai()
