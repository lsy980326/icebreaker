import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from third_parties.github import get_all_github_profile_data
from utils.color_logger import log_info, log_success, log_warning, log_process
from agents.github_lookup_agent import lookup_github_profile
from output_parsers import summary_parser


# API 키 확인
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    log_success(f"API 키 확인: 설정됨")
    log_info(f"API 키 앞 10자리: {api_key[:10]}...")
else:
    log_warning("API 키가 설정되지 않음")


def ice_break_with(name: str) -> str:
    github_username = lookup_github_profile(name=name)
    github_data = get_all_github_profile_data(username=github_username)

    summary_template = """
        다음 정보를 바탕으로 한국어로 답변해주세요:
        
        정보: {information}
        
        다음 형식으로 작성해주세요:
        1. 요약: 위 정보의 핵심 내용을 간단히 정리
        2. 흥미로운 사실: 프로젝트에 관한 2가지 흥미로운 점이나 특징
        3. 부족한점이나 개선점: 부족한점이나 개선점이 있으면 적어주세요 없으면 칭찬해줘요
        
        반드시 한국어로만 답변해주세요.
        \n{format_instructions}
    """

    # input_variables: 템플릿에 사용할 변수 비어있을 수도 있어서 리스트로 넣어줌
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    # temperature: ai가 얼마나 창의적일지 정하는 것
    # model: ai가 사용할 모델
    log_process("gpt-4.1-nano 모델 사용 중...")
    llm = ChatOpenAI(temperature=0, model="gpt-4.1-nano", api_key=api_key)

    # 파이프 연산자를 통해 summary_prompt_template에 있는 내용을 llm에 전달
    # chain = summary_prompt_template | llm

    # LangChain Expression Language
    chain = summary_prompt_template | llm | summary_parser

    # chain.invoke를 체인 실행
    log_process("AI 모델 실행 중...")
    res = chain.invoke(input={"information": github_data})
    log_info("결과:")
    print(res)


if __name__ == "__main__":
    # .env 파일 로드
    load_dotenv()
    log_success("Ice Breaker Enter")
    ice_break_with(name="yeop lsy980326")