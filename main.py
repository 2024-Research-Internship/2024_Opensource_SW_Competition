import streamlit as st
import os
from dotenv import load_dotenv

from retrieve import retrieve_from_github
from rerank import rerank_by_readme
from chat_interaction import get_intent_from_chatgpt, check_continue_chatting

# OpenAI API 키 설정
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


def main():
    # 페이지 설정
    st.set_page_config(
        page_title="GitHub Repository Recommendation System",
        layout="wide",
        page_icon="🚀"
    )

    # 페이지 제목 및 설명
    st.title('🚀 GitHub Repository Recommendation System')
    st.markdown("""
    Welcome to the **GitHub Repository Recommendation System**! 🌟  
    Chat with AI or get tailored recommendations for GitHub repositories based on your queries.  
    """)

    # 대화 내역 초기화
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []  # 메시지를 리스트로 저장

    # 왼쪽 사이드바에서 대화 내역 표시
    with st.sidebar:
        st.header("💬 Conversation History")
        conversation_container = st.empty()  # 대화 내역 컨테이너
        conversation_text = "\n".join([f"**{'User: '+m[6:] if m.startswith('User:') else 'Chat: ' + m[9:]}**\n" for m in st.session_state.conversation_history])
        conversation_container.markdown(conversation_text, unsafe_allow_html=True)

        # 입력 필드와 버튼
        st.header("🔍 User Input")
        user_query = st.text_input("Ask me anything or search for repositories:", placeholder="e.g., Can you recommend some machine learning repositories?")
        submit_button = st.button("Submit")

    # 사용자가 입력하고 제출 버튼을 눌렀을 때
    if submit_button and user_query:
        # 사용자 입력 추가
        st.session_state.conversation_history.append(f"User: {user_query}")

        # 검색 의도 판단
        stop_chat = check_continue_chatting(user_query)
        st.session_state.conversation_history.append(f"Chatbot: {stop_chat['response']}")

        # 대화 내역 업데이트
        conversation_text = "\n".join([f"**{'User: '+m[6:] if m.startswith('User:') else 'Chat: ' + m[9:]}**\n" for m in st.session_state.conversation_history])
        conversation_container.markdown(conversation_text, unsafe_allow_html=True)
        # 검색 의도가 있는 경우 처리
        if stop_chat['intent'] == 'yes':
            # 검색 의도를 추출
            intent = get_intent_from_chatgpt(user_query, "\n".join(st.session_state.conversation_history))
            st.success(f"🎯 Detected search intent.")
            st.markdown(f"**Search Keywords:** {intent['search_keywords']}  \
                         **Re-rank Keywords:** {intent['rerank_keywords']}")

            # GitHub에서 리포지토리 검색
            st.info("🔍 Fetching repositories from GitHub...")
            search_results = retrieve_from_github(intent['search_keywords'])

            if search_results:
                st.success(f"🔎 Found {len(search_results)} repositories related to your query.")
                st.info("🔧 Reranking repositories based on relevance...")
                ranked_results = rerank_by_readme(intent['rerank_keywords'], search_results)

                # 상위 5개 리포지토리 표시
                st.write("### 🏆 Top 5 Recommended Repositories")
                for i, repo in enumerate(ranked_results[:5], 1):
                    st.markdown(f"**{i}. [{repo['full_name']}]({repo['html_url']})**")
                    st.write(f"   - 📝 **Description:** {repo['description']}")
                    st.write(f"   - ⭐ **Stars:** {repo['stargazers_count']}")
                    st.write(f"   - 🍴 **Forks:** {repo['forks_count']}")
                    st.write(f"   - 📅 **Last Updated:** {repo['updated_at']}")

                    # 추천 이유 생성
                    keywords = intent['rerank_keywords']
                    recommended_reason = f"This repository is recommended because its description and README content align with keywords like: **{keywords}**."
                    st.markdown(f"   - 🤖 **Why Recommended:** {recommended_reason}")

                    readme_preview = repo['readme'][:300] if 'readme' in repo else "README not available."
                    st.markdown(f"   - 📖 **README Preview:**\n\n```markdown\n{readme_preview}\n```")
                    st.markdown(f"[🔗 Read the full README on GitHub]({repo['html_url']}/blob/main/README.md)")
                    st.markdown("---")
            else:
                st.warning("⚠️ No repositories found. Try refining your query.")

        else:
            st.info(stop_chat['response'])
            # 갱신된 대화 내역 표시
            conversation_text = "\n".join([f"**{'User: '+m[6:] if m.startswith('User:') else 'Chat: ' + m[9:]}**\n" for m in st.session_state.conversation_history])
            conversation_container.markdown(conversation_text, unsafe_allow_html=True)

    # 페이지 하단 추가 정보
    with st.container():
        st.markdown("---")
        st.markdown("""
        **Note:**  
        This system is powered by OpenAI's ChatGPT and GitHub APIs.  
        Results are based on the most recent data available.
        """)


if __name__ == "__main__":
    main()
