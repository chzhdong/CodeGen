import re
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import BaseOutputParser

class MarkdownOutputParser(BaseOutputParser):
    """
    MarkdownOutputParser is a parser for markdown output.
    """
    def parse(self, text) -> str:
        if isinstance(text, BaseMessage):
            text = text.content
        match = re.search(r"```(?:python)\n([\s\S]*?)\n```", text)
        return match.group(1).strip() if match else text.strip()
