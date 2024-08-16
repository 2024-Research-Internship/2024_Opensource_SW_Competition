import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Tuple
from openai import OpenAI
import os

# GitHub API 설정
GITHUB_API_URL = 'https://api.github.com/search/repositories'



# GitHub에서 리포지토리 검색
def retrieve_from_github(query: str) -> List[dict]:
    response = requests.get(GITHUB_API_URL, params={'q': query, 'per_page': 10})
    response.raise_for_status()
    return response.json().get('items', [])