from typing import List, Tuple
import os
import math
from sentence_transformers import CrossEncoder


model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
def readme_score(query: str, readme_content: str) -> int:
    # Crossencoder 모델을 사용한 query <-> readme score 계산

    # query가 list인 경우, string으로 변환
    if isinstance(query, list):
        query = ' '.join(query)

    inputs = [(query, readme_content)]
    scores = model.predict(inputs)
    
    print(query, scores)
    
    return scores[0]
    
    
    
# README 파일 분석 및 재순위화
def rerank_by_readme(rerank_keywords:str, repositories: List[dict]) -> List[dict]:

    scored_repos = []
    for repo in repositories:
        score = readme_score(rerank_keywords, repo['readme'])
        scored_repos.append((repo, score))
    
    # 점수를 기준으로 리포지토리 정렬
    scored_repos.sort(key=lambda x: x[1], reverse=True)
    
    #debugging
    print([(repo['full_name'],score) for repo, score in scored_repos])
    
    return [repo for repo, score in scored_repos]
