from openai import OpenAI

# OpenAI client for DeepInfra API
client = OpenAI(
    api_key="8upoXTDhgABbLwhwNHBbJHi1ucOWecUU",  # Replace with a secure method in production
    base_url="https://api.deepinfra.com/v1/openai"
)

# Chat model to use
MODEL_NAME = "Qwen/Qwen3-30B-A3B"
