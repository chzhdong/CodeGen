from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

class CodeState(TypedDict):
    query: str
    docs: List[Document]
    code: str
    error:str
    passed: bool
    prompt: List[BaseMessage]
    feedback: List[BaseMessage]
    rounds: int
