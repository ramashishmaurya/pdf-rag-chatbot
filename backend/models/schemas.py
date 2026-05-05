from pydantic import BaseModel
from typing import Optional

# this is chatschema use have session id and question
class ChatRequest(BaseModel):
    session_id :str 
    question :str 


# session_id needs to veryfield is that same guys or not 
class ChatResponse(BaseModel):
    answer : str 
    sources:list[str]
    session_id :str 

