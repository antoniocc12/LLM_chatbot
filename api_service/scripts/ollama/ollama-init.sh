#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

LLM_MODEL_NAME=${LLM_MODEL_NAME:-'phi3:mini'}
echo "Retrieve ${LLM_MODEL_NAME} model..."
ollama pull ${LLM_MODEL_NAME}
ollama create ${LLM_MODEL_NAME} -f ./scripts/ollama/Modelfile

echo "Done!"

# Wait for Ollama process to finish.
wait $pid