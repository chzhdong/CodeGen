from states.state import CodeState
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def build_prompt(state: CodeState) -> CodeState:
    messages = [
        SystemMessage(content="You are a professional programmer. Generate clean Python code based on human instructions.")
    ]
    for doc in state["docs"]:
        messages.append(HumanMessage(content=f"Instruction: {doc.page_content}"))
        messages.append(AIMessage(content=doc.metadata["code"])) 
    messages.append(HumanMessage(content=f"Instruction: {state['query']}"))
    state["prompt"] = messages
    return state

def build_feedback(state: CodeState) -> CodeState:
    messages = [
        SystemMessage(content="You are a professional programmer. Your task is to refine and correct Python code based on the user's instructions and feedback.")
    ]
    for doc in state["docs"]:
        messages.append(HumanMessage(content=f"Instruction: {doc.page_content}"))
        messages.append(AIMessage(content=doc.metadata["code"]))  
    messages.append(HumanMessage(content=f"The previously generated code was:\n{state['code']}"))
    messages.append(AIMessage(content=f"It produced the following error:\n{state['error']}"))
    messages.append(HumanMessage(content=f"Please generate a corrected version of the code based on this instruction:\n{state['query']}"))
    state["feedback"] = messages
    return state
