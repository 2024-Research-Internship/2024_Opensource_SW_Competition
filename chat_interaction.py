from openai import OpenAI
import json
# ChatGPT를 사용하여 검색용, 리랭킹용 키워드 추출
def get_intent_from_chatgpt(query: str) -> dict:
    client = OpenAI()

    PROMPT = '''From the user's request, extract two sets of keywords to optimize GitHub repository search and ranking:

1) "search_keywords": A concise set of main keywords optimized for GitHub search queries to find the most accurate and relevant repositories. These keywords should be directly applicable to GitHub's search functionality.

2) "rerank_keywords": A more detailed and comprehensive set of keywords or phrases that reflect the user's requirements more thoroughly. These will be used to re-rank repositories based on their README content.

Return the results in JSON format with the keys "search_keywords" and "rerank_keywords".

Ensure the response is concise, accurate, and suitable for direct use in GitHub search and re-ranking of repositories. Do not include any additional text or explanation.'''

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
    response = completion.choices[0].message.content
    intent = json.loads(response)
    return intent