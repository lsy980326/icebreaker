import requests
import json
import os
from collections import Counter
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


def get_all_github_profile_data(username):
    api_base = "https://api.github.com"
    headers = {"Accept": "application/vnd.github.v3+json"}

    # GitHub Personal Access Token이 있으면 Authorization 헤더 추가
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    final_data = {}

    try:
        # 1. 기본 사용자 정보 가져오기
        user_response = requests.get(f"{api_base}/users/{username}", headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()

        final_data["profile"] = {
            "login_id": user_data.get("login"),
            "name": user_data.get("name"),
            "avatar_url": user_data.get("avatar_url"),
            "image_url": user_data.get("avatar_url"),  # image_url로도 접근 가능
            "bio": user_data.get("bio"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "public_repos": user_data.get("public_repos"),
            "profile_url": user_data.get("html_url"),
        }

        # 2. 모든 저장소 정보 가져오기 (페이지네이션 고려)
        all_repos = []
        page = 1
        while True:
            repos_response = requests.get(
                f"{api_base}/users/{username}/repos?per_page=100&page={page}",
                headers=headers,
            )
            repos_response.raise_for_status()
            repos_page_data = repos_response.json()
            if not repos_page_data:
                break
            all_repos.extend(repos_page_data)
            page += 1

        if not all_repos:
            return final_data

        # 3. 인기 저장소 선정 (스타 + 포크 개수로 정렬)
        all_repos.sort(
            key=lambda r: r["stargazers_count"] + r["forks_count"], reverse=True
        )
        final_data["popular_repos"] = [
            {
                "name": repo.get("name"),
                "url": repo.get("html_url"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
            }
            for repo in all_repos[:6]
        ]  # 상위 6개

        # 4. 모든 저장소의 언어 사용량 집계
        total_language_bytes = Counter()
        for repo in all_repos:
            if not repo["fork"]:  # 포크한 저장소는 제외
                lang_response = requests.get(repo["languages_url"], headers=headers)
                if lang_response.status_code == 200:
                    for lang, bytes_count in lang_response.json().items():
                        total_language_bytes[lang] += bytes_count

        # 5. 언어 사용 비율 계산
        total_bytes = sum(total_language_bytes.values())
        language_stats = {}
        if total_bytes > 0:
            for lang, count in total_language_bytes.most_common():
                percentage = (count / total_bytes) * 100
                language_stats[lang] = round(percentage, 2)

        final_data["language_usage"] = language_stats

        return final_data

    except requests.exceptions.HTTPError as err:
        return {"error": f"API 요청 실패 (Status: {err.response.status_code})"}
    except Exception as err:
        return {"error": f"처리 중 에러 발생: {err}"}
