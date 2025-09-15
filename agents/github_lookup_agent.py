import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import (AgentExecutor, create_react_agent)
from langchain import hub
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.tools import get_profile_username_tavily
from utils.color_logger import log_info, log_success, log_warning, log_process, log_highlight, log_debug


class ColorfulAgentCallbackHandler(BaseCallbackHandler):
    """에이전트 실행 과정을 색상으로 표시하는 콜백 핸들러"""
    
    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        """에이전트가 액션을 실행할 때 호출"""
        log_process(f"생각: {action.log}")
        log_highlight(f"액션: {action.tool}")
        log_info(f"입력: {action.tool_input}")
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        """에이전트가 완료될 때 호출"""
        log_success(f"최종 답변: {finish.return_values.get('output', '')}")
    
    def on_tool_start(self, serialized, input_str: str, **kwargs) -> None:
        """도구 실행 시작 시 호출"""
        tool_name = serialized.get("name", "Unknown")
        log_process(f"도구 실행 중: {tool_name}")
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """도구 실행 완료 시 호출"""
        log_success("도구 실행 완료")
        if len(output) > 200:
            log_debug(f"결과 (요약): {output[:200]}...")
        else:
            log_debug(f"결과: {output}")


def lookup_github_profile(name: str):
    # llm 정의
    llm = ChatOpenAI(
        temperature=0, 
        model="gpt-4.1-nano", 
        api_key=os.getenv("OPENAI_API_KEY")
    )
    # 프롬프트 정의
    template = """
    주어진 이름에서 GitHub 사용자명을 찾아서 사용자명만 반환해주세요.
    
    이름: {name}
    
    중요한 지침:
    - GitHub 사용자명만 반환하세요 (추가 설명 없이)
    - 예시: "lsy980326" (O), "The GitHub username is lsy980326" (X)
    - 찾은 사용자명 그 자체만 출력하세요
    """

    # 프롬프트 템플릿 정의
    promt_template = PromptTemplate(
        template=template,
        input_variables=["name"]
    )

    # 에이전트가 사용할 모든 툴 정의
    """
    name: 에이전트가 도구를 사용할 때 사용할 이름 (추론 엔진에 표시 및 로그에 표시)
    func: 도구를 사용할 함수
    description: 도구를 사용할 때 사용할 설명 (추론 엔진에서 이 설명을 보고 사용할지 결정)
    """
    tools_for_agent = [
        Tool(
            name="get_profile_username_tavily",
            func=get_profile_username_tavily,
            description="Search for a person's Username using Tavily API"
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

    # 컬러풀 콜백 핸들러 생성
    colorful_callback = ColorfulAgentCallbackHandler()
    
    # 리액트 창시자 에이전트 실행
    """
    verbose: 에이전트 실행 시 추론 엔진에서 출력할 정보의 상세 정도
    handle_parsing_errors: 에이전트 실행 시 추론 엔진에서 출력할 정보의 상세 정도
    """
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_for_agent,
        verbose=False,  # 기본 verbose를 끄고 우리 콜백을 사용
        handle_parsing_errors=True
    )
   
    log_process(f"GitHub 프로필 검색 시작: {name}")
    
    # 결과 출력
    result = agent_executor.invoke(
        {"input": promt_template.format_prompt(name=name)}, 
        {"callbacks": [colorful_callback]}
    )
    github_username = result["output"]
    
    log_success(f"검색 완료: {github_username}")
    return github_username




if __name__ == "__main__":
    log_highlight("GitHub 에이전트 시작!")
    github_username = lookup_github_profile("lsy980326")
    log_info(f"최종 결과: {github_username}")