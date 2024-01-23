#!/bin/bash

VAULT_ADDR="${VAULT_ADDR:-http://10.32.25.213:8200}"

authenticate_with_vault() {
    read -p "Enter your Vault username: " USERNAME
    read -sp "Enter your Vault Password: " PASSWORD
    echo ""

    URL="${VAULT_ADDR}/v1/auth/userpass/login/${USERNAME}"
    RESPONSE=$(curl -k -s -X POST ${URL} -d "{\"password\": \"${PASSWORD}\"}")
    VAULT_TOKEN=$(echo $RESPONSE | jq -r '.auth.client_token')

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
    RESPONSE=$(curl -k -s -X GET ${URL} -H "X-Vault-Token: ${VAULT_TOKEN}")
    OPENAI_API_KEY=$(echo $RESPONSE | jq -r '.data.data.api_key')

    echo ${OPENAI_API_KEY}
}

slugify_input() {
    USER_INPUT=$1
    # Convert to lowercase, replace spaces with dashes, and keep alphanumeric characters and dashes
    SLUGIFIED_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')
    # Ensure the filename is no longer than 30 characters
    echo ${SLUGIFIED_INPUT:0:30}
}

save_to_markdown() {
    SLUGIFIED_INPUT=$1
    USER_INPUT=$2
    RESPONSE=$3
    DIRECTORY="conversations"

    # Create the directory if it doesn't exist
    [ ! -d $DIRECTORY ] && mkdir $DIRECTORY

    FILENAME="${DIRECTORY}/${SLUGIFIED_INPUT}_$(date +%Y%m%d_%H%M%S).md"
    echo -e "# ${USER_INPUT}\n\n- **You:** ${USER_INPUT}\n- **ChatGPT:** ${RESPONSE}" > $FILENAME
}

save_conversation() {
    CONVERSATION_HISTORY_JSON=$1
    FILENAME="conversations/conversation_$(date +%Y%m%d_%H%M%S).md"

    # Save the conversation history to a markdown file
    echo "$CONVERSATION_HISTORY_JSON" | jq -r '.[] | "- **\(.role):** \(.content)"' > "$FILENAME"
    echo "Conversation saved to $FILENAME"
}

exit_handler() {
    echo ""
    echo "Exiting and saving conversation..."
    save_conversation "$CONVERSATION_HISTORY"
    exit
}

chat_with_openai() {
    OPENAI_KEY=$1
    CONVERSATION_HISTORY="[]"

    # Trap the SIGINT signal to handle CTRL+C
    trap exit_handler SIGINT

    while true; do
        echo ""
        read -p "You: " USER_INPUT

        # Add user message to conversation history
        CONVERSATION_HISTORY=$(echo $CONVERSATION_HISTORY | jq --arg role "user" --arg content "$USER_INPUT" '. += [{"role": $role, "content": $content}]')

        # Get response from OpenAI
        RESPONSE_JSON=$(curl -s -X POST https://api.openai.com/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $OPENAI_KEY" \
            -d "{
                \"model\": \"gpt-4\",
                \"messages\": $CONVERSATION_HISTORY
            }")
        
        # Extract and display the assistant’s response
        RESPONSE=$(echo $RESPONSE_JSON | jq -r ".choices[0].message.content")
        echo ""
        echo "ChatGPT: $RESPONSE"
        echo ""
        
        # Add assistant’s response to conversation history
        CONVERSATION_HISTORY=$(echo $CONVERSATION_HISTORY | jq --arg role "assistant" --arg content "$RESPONSE" '. += [{"role": $role, "content": $content}]')
        
        # Save the conversation to a markdown file
        SLUGIFIED_INPUT=$(slugify_input "$USER_INPUT")
        save_to_markdown $SLUGIFIED_INPUT "$USER_INPUT" "$RESPONSE"
    done
}


if [ "$0" == "${BASH_SOURCE[0]}" ]; then
    VAULT_TOKEN=$(authenticate_with_vault)
    OPENAI_API_KEY=$(get_openai_api_key ${VAULT_TOKEN})
    chat_with_openai ${OPENAI_API_KEY}
fi
