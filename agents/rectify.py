from states.state import CodeState
from tools.mdParser import MarkdownParser

def build_correct_node(llm_model):
    def correct_code(state: CodeState) -> CodeState:
        response = llm_model.invoke(state["feedback"])
        parser = MarkdownParser()
        state["code"] = parser.parse(response.content)
        state["rounds"] += 1
        return state
    return correct_code
