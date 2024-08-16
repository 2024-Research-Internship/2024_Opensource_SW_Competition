import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Tuple
from openai import OpenAI
import os

def readme_score(readme_content: str) -> int:
        # 간단한 분석 예: README의 단어 수를 사용한 점수 매기기
    return len(readme_content.split())
    
    
    
# README 파일 분석 및 재순위
def rerank_by_readme(repositories: List[dict]) -> List[dict]:

    scored_repos = []
    for repo in repositories:
        readme_url = repo['contents_url'].replace('{+path}', 'README.md')
        try:
            readme_response = requests.get(readme_url)
            readme_content = readme_response.text
            score = readme_score(readme_content)
            scored_repos.append((repo, score))
        except Exception as e:
            st.write(f"Error fetching README for {repo['full_name']}: {e}")
    
    # 점수를 기준으로 리포지토리 정렬
    scored_repos.sort(key=lambda x: x[1], reverse=True)
    return [repo for repo, score in scored_repos]
