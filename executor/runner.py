from classes.state import CodeState

def py_checker(state: CodeState) -> CodeState:
    code = state.code
    try:
        compile(code, filename="<string>", mode="exec")
        state.passed = True
        state.error = f"Program is correct.\n"
        return state
    except SyntaxError as e:
        state.passed = False
        state.error = f"Program exists syntax errors: \n{e}"
        return state
    except Exception as e:
        state.passed = False
        state.error = f"Program exists errors: \n{e}"
        return state
