from typing import List
from pydantic import BaseModel,Field,validator
 
class MCQQuestion(BaseModel):

    question: str = Field(description="The question to be answered")

    options: List[str] = Field(description="The options to choose from")

    correct_answer: str = Field(description="The correct option from the options list")

    @validator("question", pre=True)
    def clean_question(cls,v):
        if isinstance(v,dict):
            return v.get("description", str(v))
        return str(v)


class FillInTheBlankQuestion(BaseModel):

    question: str = Field(description="The question to be answered with '___' for the blank")

    answer: str = Field(description="The answer to the question in a word or phrase for the blank")
    
    @validator("question", pre=True)
    def clean_question(cls,v):
        if isinstance(v,dict):
            return v.get("description", str(v))
        return str(v)