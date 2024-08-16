import streamlit as st
import os


from retrieve import retrieve_from_github
from rerank import rerank_by_readme
from chat_interaction import get_intent_from_chatgpt

# OpenAI API 키 설정
os.environ['OPENAI_API_KEY']=None



import streamlit as st
from PIL import Image

def main():
    # Set the title and layout of the app
    st.set_page_config(page_title="GitHub Repository Recommendation System", layout="wide")
    st.title('🚀 GitHub Repository Recommendation System')

    # Add a subheader and a brief description
    st.subheader("Find the best GitHub repositories tailored to your needs")
    st.markdown("""
    This tool helps you discover the most relevant GitHub repositories based on your query. 
    Whether you're searching for code examples, open-source projects, or tools, we've got you covered!
    """)

    # Get user input
    st.write("### 🔍 Search for Repositories")
    user_query = st.text_input('Enter your query:', placeholder="e.g., machine learning, data visualization")

    if st.button('Get Recommendations'):
        if user_query:
            with st.spinner('Analyzing your query and fetching the best repositories...'):
                # 1. Identify user intent using ChatGPT API
                intent = get_intent_from_chatgpt(user_query)
                st.success(f'🎯 Intent identified: **{intent}**')

                # 2. Fetch GitHub search results
                search_results = retrieve_from_github(user_query)
                st.success(f'🔎 Found **{len(search_results)}** repositories related to your query.')

                st.info("🔧 **Reranking repositories according to your preferences...**")
                # 3. Analyze and rerank repositories by README content
                ranked_results = rerank_by_readme(search_results)
                st.write("### 🏆 Top 5 Recommended Repositories")
                for i, repo in enumerate(ranked_results[:5], 1):
                    st.markdown(f"**{i}. [{repo['full_name']}]({repo['html_url']})**")
                    st.write(f"   - 📝 **Description:** {repo['description']}")
                    st.write(f"   - ⭐ **Stars:** {repo['stargazers_count']}")
                    st.write(f"   - 🍴 **Forks:** {repo['forks_count']}")
                    st.write(f"   - 📅 **Last Updated:** {repo['updated_at']}")
        else:
            st.warning('⚠️ Please enter a query to get recommendations.')

    # Add a footer
    st.markdown("""
                ---
                **Note:** This tool is powered by OpenAI's ChatGPT and GitHub APIs. The results are based on the most recent data available.
                """)


if __name__ == "__main__":
    main()