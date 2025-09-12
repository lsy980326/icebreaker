"""
컬러 로깅을 위한 유틸리티 모듈
"""
import os
from colorama import init, Fore, Back, Style

# colorama 초기화 (Windows 지원)
init(autoreset=True)

class ColorLogger:
    """터미널에 색상이 있는 로그를 출력하는 클래스"""
    
    @staticmethod
    def success(message):
        """성공 메시지 (초록색)"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def info(message):
        """정보 메시지 (파란색)"""
        print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(message):
        """경고 메시지 (노란색)"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def error(message):
        """에러 메시지 (빨간색)"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def debug(message):
        """디버그 메시지 (회색)"""
        print(f"{Fore.LIGHTBLACK_EX}🔍 {message}{Style.RESET_ALL}")
    
    @staticmethod
    def highlight(message):
        """강조 메시지 (마젠타색)"""
        print(f"{Fore.MAGENTA}🌟 {message}{Style.RESET_ALL}")
    
    @staticmethod
    def process(message):
        """처리 중 메시지 (노란색 배경)"""
        print(f"{Back.YELLOW}{Fore.BLACK}⏳ {message}{Style.RESET_ALL}")

# 편의를 위한 전역 함수들
def log_success(message):
    ColorLogger.success(message)

def log_info(message):
    ColorLogger.info(message)

def log_warning(message):
    ColorLogger.warning(message)

def log_error(message):
    ColorLogger.error(message)

def log_debug(message):
    ColorLogger.debug(message)

def log_highlight(message):
    ColorLogger.highlight(message)

def log_process(message):
    ColorLogger.process(message)

if __name__ == "__main__":
    # 테스트
    print("=== 컬러 로거 테스트 ===")
    log_success("성공적으로 완료되었습니다!")
    log_info("정보를 표시합니다.")
    log_warning("주의가 필요합니다.")
    log_error("오류가 발생했습니다.")
    log_debug("디버그 정보입니다.")
    log_highlight("중요한 내용입니다!")
    log_process("처리 중입니다...")
