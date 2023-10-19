#!/bin/bash

VAULT_ADDR="${VAULT_ADDR:-http://10.32.25.213:8200}"

authenticate_with_vault() {
    read -p "Enter your Vault username: " USERNAME
    read -sp "Enter your Vault Password: " PASSWORD
    echo ""

    URL="${VAULT_ADDR}/v1/auth/userpass/login/${USERNAME}"
    VAULT_TOKEN=$(curl -k -s -X POST ${URL} -d "{\"password\": \"${PASSWORD}\"}" | jq -r '.auth.client_token')

    if [ "${VAULT_TOKEN}" == "null" ]; then
        echo "Failed to retrieve Vault token"
        exit 1
    fi

    echo ${VAULT_TOKEN}
}

get_openai_api_key() {
    VAULT_TOKEN=$1
    SECRET_PATH="kv/data/openai"
    URL="${VAULT_ADDR}/v1/${SECRET_PATH}"
    OPENAI_API_KEY=$(curl -k -s -X GET ${URL} -H "X-Vault-Token: ${VAULT_TOKEN}" | jq -r '.data.data.api_key')

    echo ${OPENAI_API_KEY}
}

chat_with_openai() {
    OPENAI_KEY=$1

    while true; do
        echo ""
        read -p "You: " USER_INPUT

        RESPONSE=$(curl -s -X POST https://api.openai.com/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $OPENAI_KEY" \
            -d "{
                \"model\": \"gpt-3.5-turbo\",
                \"messages\": [{
                    \"role\": \"user\",
                    \"content\": \"$USER_INPUT\"
                }]
            }" | jq -r ".choices[0].message.content")
        echo ""
        echo "ChatGPT: $RESPONSE"
        echo ""
    done
}

if [ "$0" == "${BASH_SOURCE[0]}" ]; then
    VAULT_TOKEN=$(authenticate_with_vault)
    OPENAI_API_KEY=$(get_openai_api_key ${VAULT_TOKEN})
    chat_with_openai ${OPENAI_API_KEY}
fi
