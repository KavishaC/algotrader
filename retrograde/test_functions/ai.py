
from openai import OpenAI

client = OpenAI(api_key="",)

chat_completion = client.chat.completions.create(
messages=[
    {
        "role": "user",
        "content": "Say this is a test",
    }],
    model="gpt-3.5-turbo",
)
print("AI response:", chat_completion)
