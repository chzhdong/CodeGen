import json
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def get_prompt(docs, query):
    messages = [
        SystemMessage(content="You are a professional programmer. Generate clean Python code based on human instructions.")
    ]
    
    for doc in docs:
        messages.append(HumanMessage(content=f"Instruction: {doc.page_content}"))
        messages.append(AIMessage(content=doc.metadata["code"]))
        
    messages.append(HumanMessage(content=f"Instruction: {query}"))
    
    return messages

def get_feedback(docs, query, code, error):
    messages = [
        SystemMessage(content="You are a professional programmer. Your task is to refine and correct Python code based on the user's instructions and feedback.")
    ]

    for doc in docs:
        messages.append(HumanMessage(content=f"Instruction: {doc.page_content}"))
        messages.append(AIMessage(content=doc.metadata["code"]))
        
    messages.append(HumanMessage(content=f"The previously generated code was:\n{code}"))
    messages.append(AIMessage(content=f"It produced the following error:\n{error}"))
    
    messages.append(HumanMessage(content=f"Please generate a corrected version of the code based on this instruction:\n{query}"))
    
    return messages
