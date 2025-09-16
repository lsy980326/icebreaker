from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Summary(BaseModel):
    name: str = Field(description="사용자 이름")
    summary: str = Field(description="요약")
    interesting_facts: List[str] = Field(description="흥미로운 사실들")
    areas_for_improvement: str = Field(description="개선점이나 칭찬")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary, 
            "interesting_facts": self.interesting_facts,
            "areas_for_improvement": self.areas_for_improvement
        }

summary_parser = PydanticOutputParser(pydantic_object=Summary)
