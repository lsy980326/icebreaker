# IceBreaker - LangChain 기반 AI 텍스트 요약 프로젝트

이 프로젝트는 LangChain을 사용하여 다양한 AI 모델로 텍스트를 요약하는 예제 프로젝트입니다. OpenAI, Mistral, Ollama 등 다양한 LLM을 지원합니다.

## 🚀 주요 기능

- **다중 AI 모델 지원**: OpenAI GPT, Mistral, Ollama (Llama3) 모델 사용
- **텍스트 요약**: 주어진 정보를 한국어로 요약하고 흥미로운 사실 추출
- **LinkedIn 프로필 스크래핑**: Proxycurl API를 통한 LinkedIn 프로필 데이터 수집
- **환경 변수 관리**: `.env` 파일을 통한 API 키 관리

## 📁 프로젝트 구조

```
IceBreaker/
├── ice_breaker_openai.py      # OpenAI GPT 모델을 사용한 텍스트 요약
├── ice_breaker_mistral.py     # Mistral 모델을 사용한 텍스트 요약
├── ice_breaker_ollama.py      # Ollama Llama3 모델을 사용한 텍스트 요약
├── third_parties/
│   └── linkedin.py            # LinkedIn 프로필 스크래핑 유틸리티
├── Pipfile                    # pipenv 의존성 관리 파일
├── .vscode/
│   └── launch.json           # VS Code 디버깅 설정
└── README.md
```

## 🛠️ 설치 및 설정

### 1. 저장소 클론

```bash
git clone <repository-url>
cd IceBreaker
```

### 2. 가상환경 설정 및 의존성 설치

```bash
# pipenv 설치 (아직 설치되지 않은 경우)
pip install pipenv

# 가상환경 생성 및 의존성 설치
pipenv install

# 가상환경 활성화
pipenv shell
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 필요한 API 키를 설정하세요:

```env
# OpenAI API 키 (ice_breaker_openai.py용)
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎯 사용법

### OpenAI 모델 사용

```bash
python ice_breaker_openai.py
```

### Mistral 모델 사용 (Ollama 필요)

```bash
# Ollama 설치 및 Mistral 모델 다운로드
ollama pull mistral

# 실행
python ice_breaker_mistral.py
```

### Llama3 모델 사용 (Ollama 필요)

```bash
# Ollama 설치 및 Llama3 모델 다운로드
ollama pull llama3

# 실행
python ice_breaker_ollama.py
```

### LinkedIn 프로필 스크래핑

```bash
python third_parties/linkedin.py
```

## 📋 의존성

- **langchain**: LangChain 핵심 라이브러리
- **langchain-openai**: OpenAI 모델 통합
- **langchain-ollama**: Ollama 모델 통합
- **python-dotenv**: 환경 변수 관리
- **requests**: HTTP 요청 처리

## 🔧 개발 환경

- **Python**: 3.12
- **패키지 관리**: pipenv
- **IDE**: VS Code (디버깅 설정 포함)

## 📝 예제

프로젝트는 Elden Ring의 "Shadow of the Erdtree" DLC에 대한 정보를 요약하는 예제를 포함하고 있습니다. 각 모델은 다음과 같은 형식으로 응답합니다:

1. **요약**: 핵심 내용을 간단히 정리
2. **흥미로운 사실**: 2가지 흥미로운 점이나 특징
