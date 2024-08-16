from openai import OpenAI

# ChatGPT를 사용하여 의도 파악
def get_intent_from_chatgpt(query: str) -> str:
    client = OpenAI()

    PROMPT = '''Extract some keywords from query. Answer Only Keywords.'''

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{PROMPT}"},
            {
                "role": "user",
                "content": f"{query}"
            }
        ]
    )
    return completion.choices[0].message.content