import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to call OpenAI's chat completion API
# This function takes a system prompt, user prompt, temperature, and max tokens as parameters
# and returns the response from the model.

def call_openai(system_prompt, user_prompt, temperature=0.5, max_tokens=200):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
