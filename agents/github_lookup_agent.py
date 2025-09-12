import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import (AgentExecutor, create_react_agent)
from langchain import hub
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.tools import get_profile_url_tavily


def lookup_github_profile(username: str):
    # llm 정의
    llm = ChatOpenAI(
        temperature=0, 
        model="gpt-4.1-nano", 
        api_key=os.getenv("OPENAI_API_KEY")
    )
    # 프롬프트 정의
    template = """
    given a github username: {username}
    """

    # 프롬프트 템플릿 정의
    promt_template = PromptTemplate(
        template=template,
        input_variables=["username"]
    )

    # 에이전트가 사용할 모든 툴 정의
    """
    name: 에이전트가 도구를 사용할 때 사용할 이름 (추론 엔진에 표시 및 로그에 표시)
    func: 도구를 사용할 함수
    description: 도구를 사용할 때 사용할 설명 (추론 엔진에서 이 설명을 보고 사용할지 결정)
    """
    tools_for_agent = [
        Tool(
            name="get_profile_url_tavily",
            func=get_profile_url_tavily,
            description="Search for a person's profile URL using Tavily API"
        )
    ]

    # 리액트 창시자 프롬프트 가져오기 (추론 엔진에서 사용)
    react_prompt = hub.pull("hwchase17/react")

    # 리액트 창시자 에이전트 생성
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    # 리액트 창시자 에이전트 실행
    """
    verbose: 에이전트 실행 시 추론 엔진에서 출력할 정보의 상세 정도
    handle_parsing_errors: 에이전트 실행 시 추론 엔진에서 출력할 정보의 상세 정도
    """
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True
    )
   
    # 결과 출력
    result = agent_executor.invoke({"input": promt_template.format_prompt(username=username)})
    github_url = result["output"]
    return github_url




if __name__ == "__main__":
    github_url = lookup_github_profile("lsy980326")
    print(github_url)