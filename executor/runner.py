def py_checker(code: str) -> tuple[bool, str]:
    try:
        compile(code, filename="<string>", mode="exec")
        return True, "Program is correct.\n"
    except SyntaxError as e:
        return False, f"Program exists syntax errors: \n{e}"
    except Exception as e:
        return False, f"Program exists errors: \n{e}"
