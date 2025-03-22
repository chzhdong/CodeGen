from parser.markdown import MarkdownOutputParser

def build_refine_node(llm_model):
    def refine_code(state: CodeGenState) -> CodeGenState:
        refined_response = llm.invoke(state.feedback)
        parser = MarkdownOutputParser()
        state.code = parser.parse(refined_response.content)
        state.rounds += 1
        return state
    
    return refine_code
