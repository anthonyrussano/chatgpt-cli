import os
import requests
import json
import openai
from getpass import getpass

VAULT_ADDR = os.environ.get("VAULT_ADDR", "https://10.32.25.213:8200")

def authenticate_with_vault(username, password):
    url = f"{VAULT_ADDR}/v1/auth/userpass/login/{username}"
    data = {"password": password}
    response = requests.post(url, json=data, verify=False)  # Retained verify=False as requested
    try:
        return response.json()['auth']['client_token']
    except (KeyError, json.JSONDecodeError):
        print("Failed to retrieve Vault token")
        exit(1)

def get_openai_api_key(vault_token):
    secret_path = 'kv/data/openai'
    headers = {'X-Vault-Token': vault_token}
    url = f"{VAULT_ADDR}/v1/{secret_path}"
    response = requests.get(url, headers=headers, verify=False) # Retained verify=False as requested
    return json.loads(response.text)['data']['data']['api_key']

def chat_with_openai():
    conversation = [
        {"role": "system", "content": "You are a DevOps assistant with expertise in Debian Linux environments..."}
    ]

    try:
        while True:
            user_input = input("You: ")
            conversation.append({"role": "user", "content": user_input})

            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
            model_response = response['choices'][0]['message']['content']
            print(f"ChatGPT: {model_response}")
            conversation.append({"role": "assistant", "content": model_response})

            save_response = input("Would you like to save this response to a text file? (yes/no): ").strip().lower()
            if save_response == "yes":
                file_name = input("Enter the filename (including path) to save the response: ").strip()
                with open(file_name, "w") as file:
                    file.write(model_response)
                print(f"Response saved to {file_name}")

    except KeyboardInterrupt:
        print("\nConversation ended by user.")

if __name__ == "__main__":
    USERNAME = input("Enter your Vault username: ")
    PASSWORD = getpass("Enter your Vault Password: ")
    VAULT_TOKEN = authenticate_with_vault(USERNAME, PASSWORD)
    openai_api_key = get_openai_api_key(VAULT_TOKEN)
    openai.api_key = openai_api_key
    chat_with_openai()
