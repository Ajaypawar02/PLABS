from typing import Optional, List
from pydantic import BaseModel, Field
from typing import List, Union, Optional

class SUMMARYPARAMETERS(BaseModel):
    text : str
    model: str = Field(default="gpt-4", example="gpt-4")


class GENERATIONPARAMETERS(BaseModel):
    model_id: str = Field(default="gpt-4", example="gpt-4")
    article_type: str = Field(default="news report", example="new")
    Description: str = Field(default="Write a news report on the recent events in the world", example="Write a news report on the recent events in the world")
    tone: str = Field(default="polite", example="polite")
                                          
    
    language: str = Field(default="en", example="en")
    
    use_internet: bool = Field(default=False, example=False)
    