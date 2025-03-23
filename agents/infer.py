from states.state import CodeState
from tools.mdParser import MarkdownParser

def build_generate_node(llm_model):
    def code_inference(state: CodeState) -> CodeState:
        response = llm_model.invoke(state["prompt"])
        parser = MarkdownParser()
        state["code"] = parser.parse(response.content)
        print(state["code"] + "\n")
        return state
    return code_inference
