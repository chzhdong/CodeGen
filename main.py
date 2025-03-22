import os
import warnings
from agents.agent import core

warnings.filterwarnings("ignore", category=UserWarning)

os.environ['LANGSMITH_TRACING']='true'
os.environ['LANGSMITH_API_KEY']='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'

if __name__ == "__main__":
    print("Welcome to local intelligent Agent")
    while True:
        instruction = input("Please input your instructions: \n>>> ")
        if instruction.lower() == "exit":
            break
        core(instruction)
