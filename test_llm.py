from src.llm.llama_client import LlamaClient

print("Creating Llama Client...")
llm = LlamaClient()

print("Calling LLM...")
response = llm.generate("What is cancer?")

print("\n====================")
print(response)
print("====================")