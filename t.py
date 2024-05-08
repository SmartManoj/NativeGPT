# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://192.168.1.10:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="TheBloke/phi-2-GGUF/phi-2.Q4_K_S.gguf",
  messages=[
    # {"role": "system", "content": "Always answer in rhymes."},
    {"role": "user", "content": "5+5"}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)