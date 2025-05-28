from pydantic import BaseModel
from typing import List, Any

class TextIn(BaseModel):
    text: str
 
class AnalyzeOut(BaseModel):
    intent: str
    entities: List[Any] 