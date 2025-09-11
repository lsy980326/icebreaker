import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """ scrape profile from linkedin"""

    # mock 옵션이 없으면 gist에 있는 목데이터로 진행
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/lsy980326/7b5dea887f800734890c013f39a6100d/raw/3dabf4b6efccfe41abacc061117a8aa9d7674af9/gistfile1.txt"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
        data = response.json()
        data = {
            k:v for k,v in data.items()
            if v not in ([],"","",None)
            and k not in ("people_also_viewed","certifications")
        }
        if data.get("group"):
            for group_dict in data.get("gropus"):
                group_dict.pop("profile_pic_url")

        
        return data
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {
            "Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"
        }
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )

        data = response.json()
        return data

        
if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://www.linkedin.com/in/eden-marco/",mock=True
        )
    )