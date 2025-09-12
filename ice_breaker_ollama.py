import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from utils.color_logger import log_info, log_success, log_process

# .env 파일 로드
load_dotenv()

information = """
Shadow of the Erdtree is a fully fledged expansion for Elden Ring
 that adds a whole new map with 70 new Weapons, 10 new Shields,
  39 new Talismans, 14 new Sorceries, 28 new Incantations, 
  20 new Spirit Ashes, 25 new Ashes of War, 
  30 new Armor Sets and new Consumables & Craftables. 
  The expansion was announced via Twitter by the official Elden Ring 
  account on February 28th, 2023. A Gameplay Trailer released on February 
  21st 2024, and a Story Trailer followed on May 21st, 2024. 
  The release date of the DLC was June 21st, 2024.
"""

if __name__ == "__main__":
    log_success("Hello, langchain!")

    summary_template = """
        다음 정보를 바탕으로 한국어로 답변해주세요:
        
        정보: {information}
        
        다음 형식으로 작성해주세요:
        1. 요약: 위 정보의 핵심 내용을 간단히 정리
        2. 흥미로운 사실: 2가지 흥미로운 점이나 특징
        
        반드시 한국어로만 답변해주세요.
    """

    # input_variables: 템플릿에 사용할 변수 비어있을 수도 있어서 리스트로 넣어줌
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # temperature: ai가 얼마나 창의적일지 정하는 것
    # model: ai가 사용할 모델
    log_process("llama3 모델 사용 중...")
    llm = OllamaLLM(model="llama3")

    # 파이프 연산자를 통해 summary_prompt_template에 있는 내용을 llm에 전달
    chain = summary_prompt_template | llm | StrOutputParser()

    # chain.invoke를 체인 실행
    log_process("AI 모델 실행 중...")
    res = chain.invoke(input={"information": information})
    log_info("결과:")
    print(res)
