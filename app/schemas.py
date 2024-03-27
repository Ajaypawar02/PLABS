from typing import Optional, List
from pydantic import BaseModel, Field
from typing import List, Union, Optional

class SUMMARYPARAMETERS(BaseModel):
    text : str
    model: str = Field(default="gpt-4", example="gpt-4")


class GENERATIONPARAMETERS(BaseModel):
    model_id: str = Field(default="gpt-4", example="gpt-4")
    article_type: str = Field(default="new", example="new")
    target_keyword: str = Field(default="health", example="health")
    secondary_keyword: List[str] = Field(default=["health care facilities", "India Situations for health", "Yojana schemes for health"], 
                                          example=["health care facilities", "India Situations for health", "Yojana schemes for health"])
    article_length: str = Field(default="long_form", example="long_form")
    tone: str = Field(default="polite", example="polite")
    language: str = Field(default="en", example="en")
    country: str = Field(default="sb", example="sb")
    pov: str = Field(default="first person", example="first person")
    use_internet: bool = Field(default=False, example=False)
    create_outline: bool = Field(default=True, example=True)
    include_faq: Optional[bool] = Field(default=False, example=False)
    include_key_takeaways: Optional[bool] = Field(default=True, example=True)
    streaming: Optional[bool] = Field(default=True, example=True)
    auto_link : bool
    image : bool