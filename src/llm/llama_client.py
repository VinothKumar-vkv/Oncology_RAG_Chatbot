import ollama
import traceback
import time


class LlamaClient:

    def __init__(self):
        # Installed Ollama model
        self.model = "qwen2.5:latest"

    def generate(self, prompt):
        print(">>> INSIDE LLAMA_CLIENT.GENERATE <<<")

        try:

            print("\n========== OLLAMA REQUEST ==========")
            print(f"Model : {self.model}")
            print(f"Prompt Length : {len(prompt)} characters")

            start = time.time()

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert oncology assistant.\n"
                            "Answer ONLY using the supplied medical evidence.\n"
                            "Do not hallucinate.\n"
                            "If evidence is insufficient, explicitly state that.\n"
                            "Always cite textbook pages, PubMed papers, and "
                            "knowledge graph facts whenever available."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            end = time.time()

            print(f"Ollama completed in {end - start:.2f} seconds")
            print("====================================\n")

            return response["message"]["content"]

        except Exception:

            print("\n========== OLLAMA FULL ERROR ==========")
            traceback.print_exc()
            print("=======================================\n")

            return "Unable to generate a response."