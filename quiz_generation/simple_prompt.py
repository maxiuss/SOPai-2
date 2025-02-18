import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_text = "Hello AI, please summarize the concept of photosynthesis."

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful tutor specialized in biology."},
        {"role": "user", "content": prompt_text}
    ]
)

output = response.choices[0].message["content"]
print("Response:")
print(output)

# Write the output to a file for persistent logging
with open("output.log", "w") as f:
    f.write(output)


