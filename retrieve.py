import requests
from typing import List, Tuple
#from dotenv import load_dotenv
#import os

# GitHub API 설정
GITHUB_API_URL = 'https://api.github.com/search/repositories'


# GitHub에서 리포지토리 검색
def retrieve_from_github(query: str) -> List[dict]:
    # Step 1. Get Repository URL from github
    
    if not isinstance(query,list):
        query = query.split(" ")    
    
    total_repo = list()
    for q in query:
        response = requests.get(GITHUB_API_URL, params={'q': q, 'per_page': 10}) #can change to 100
        response.raise_for_status()
        repositories = response.json().get('items', [])

        # Step 2: Retrieve README for each repository
        for repo in repositories:
            repo_name = repo['full_name']
            readme_url = f"https://api.github.com/repos/{repo_name}/readme"
            readme_response = requests.get(readme_url, headers={'Accept': 'application/vnd.github.v3.raw'})
            
            if readme_response.status_code == 200:
                repo['readme'] = readme_response.text
            else:
                repo['readme'] = "README not found or not accessible."
        
        total_repo+=repositories
        
    return total_repo