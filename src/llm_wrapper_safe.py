import os
from mistralai import Mistral
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the environment variable
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("Missing MISTRAL_API_KEY in environment variables")

# Initialize client
client = Mistral(api_key=api_key)

def query_model(prompt: str, system: str = "You are Julien Vaughan. Answer as him.") -> str:
    """
    Query the Mistral chat completion API with a deterministic setting.
    """
    response = client.chat.complete(
        model="mistral-medium",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    # Access the content attribute of the message object
    return response.choices[0].message.content.strip()

