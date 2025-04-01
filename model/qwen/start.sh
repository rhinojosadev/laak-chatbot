#!/bin/sh
../bin/ollama serve &
pid=$!
sleep 5
echo "Pulling qwen2.5 model"
ollama pull qwen2.5:3b
wait $pid