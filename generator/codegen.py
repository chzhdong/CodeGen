from parser.markdown import MarkdownOutputParser

def build_generate_node(llm_model):
    def generate_code(state: CodeState) -> CodeState:
        response = llm_model.invoke(state.prompt)
        output = response.content
        parser = MarkdownOutputParser()
        state.code = parser.parse(output)
        return state
    return generate_code
