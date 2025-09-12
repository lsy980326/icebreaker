from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv()

def get_profile_url_tavily(name: str):
    """Search for a person's profile URL using Tavily API"""
    api_key = os.getenv("TAVILY_API_KEY")
    
    # API 키가 없으면 기본 메시지 반환
    if not api_key:
        return f"GitHub profile search for: {name} (Tavily API key not configured)"
    
    # API 키가 있으면 TavilySearchResults 초기화
    search = TavilySearchResults(tavily_api_key=api_key)
    
    # 더 구체적인 GitHub 검색 쿼리 사용
    search_query = f"site:github.com {name} profile"
    res = search.run(search_query)
    
    # 결과가 있으면 첫 번째 결과의 URL 반환, 없으면 기본 메시지
    if res and len(res) > 0:
        return res
    else:
        return f"No GitHub profile found for username: {name}"  