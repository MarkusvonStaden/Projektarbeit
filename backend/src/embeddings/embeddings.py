import requests

def create_embedding(text: str, model: str = "mxbai-embed-large"):
    response = requests.post(
        "http://ollama:11434/api/embed",
        json={
            "model": model,
            "input": text
        }
    )
    if response.status_code == 200:
        return response.json().get("embeddings")[0]
    else:
        raise Exception(f"Error creating embedding: {response.text}")