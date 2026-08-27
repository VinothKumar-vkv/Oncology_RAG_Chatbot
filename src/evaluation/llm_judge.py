"""
llm_judge.py

LLM-as-a-Judge Evaluation Metrics for Oncology Agentic RAG

Metrics:
1. Faithfulness
2. Answer Relevancy
3. Context Precision
4. Context Recall

Author: Haritha
"""

import re
from src.llm.llama_client import LlamaClient


class LLMJudge:
    def __init__(self):
        self.llm = LlamaClient()

    def _extract_score(self, response: str) -> float:
        """
        Extract numeric score from LLM response.

        Expected:
        95
        95.5
        Score: 92
        """

        match = re.search(r"(\d+(\.\d+)?)", response)

        if match:
            score = float(match.group(1))
            score = max(0, min(score, 100))
            return round(score, 2)

        return 0.0

    def _ask_llm(self, prompt: str) -> float:
        response = self.llm.generate(prompt)
        return self._extract_score(response)

    #######################################################################
    # 1. Faithfulness
    #######################################################################

    def faithfulness(self, context: str, answer: str) -> float:

        prompt = f"""
You are an expert evaluator.

Retrieved Context:
{context}

Generated Answer:
{answer}

Evaluate ONLY how well the answer is supported by the retrieved context.

Score Guidelines:

100 = Completely supported.
80 = Mostly supported.
60 = Partially supported.
40 = Many unsupported statements.
20 = Mostly hallucinated.
0 = Completely incorrect.

Return ONLY one number between 0 and 100.
"""

        return self._ask_llm(prompt)

    #######################################################################
    # 2. Answer Relevancy
    #######################################################################

    def answer_relevancy(self, question: str, answer: str) -> float:

        prompt = f"""
Question:
{question}

Generated Answer:
{answer}

Evaluate how well the answer addresses the user's question.

Score Guidelines:

100 = Perfect answer.
80 = Good answer.
60 = Partially answers.
40 = Weak answer.
20 = Mostly irrelevant.
0 = Completely irrelevant.

Return ONLY one number between 0 and 100.
"""

        return self._ask_llm(prompt)

    #######################################################################
    # 3. Context Precision
    #######################################################################

    def context_precision(self, question: str, context: str) -> float:

        prompt = f"""
Question:
{question}

Retrieved Context:
{context}

Evaluate how much of the retrieved context is actually useful for answering the question.

100 = All context is relevant.
80 = Mostly relevant.
60 = Moderately relevant.
40 = Large irrelevant portions.
20 = Mostly irrelevant.
0 = Completely irrelevant.

Return ONLY one number between 0 and 100.
"""

        return self._ask_llm(prompt)

    #######################################################################
    # 4. Context Recall
    #######################################################################

    def context_recall(
        self,
        reference_answer: str,
        context: str
    ) -> float:

        prompt = f"""
Reference Answer:
{reference_answer}

Retrieved Context:
{context}

Evaluate how much of the information needed to produce the reference answer exists inside the retrieved context.

100 = All information present.
80 = Most information present.
60 = Moderate information present.
40 = Missing many facts.
20 = Very little information.
0 = No useful information.

Return ONLY one number between 0 and 100.
"""

        return self._ask_llm(prompt)

    #######################################################################
    # Complete Evaluation
    #######################################################################

    def evaluate(
        self,
        question,
        context,
        generated_answer,
        reference_answer
    ):

        return {

            "Faithfulness (%)":
                self.faithfulness(
                    context,
                    generated_answer
                ),

            "Answer Relevancy (%)":
                self.answer_relevancy(
                    question,
                    generated_answer
                ),

            "Context Precision (%)":
                self.context_precision(
                    question,
                    context
                ),

            "Context Recall (%)":
                self.context_recall(
                    reference_answer,
                    context
                )
        }


###########################################################################
# Example
###########################################################################

if __name__ == "__main__":

    judge = LLMJudge()

    question = "What is breast cancer?"

    context = """
Breast cancer begins in breast tissue.
Treatment includes surgery, chemotherapy,
radiotherapy and hormonal therapy.
"""

    answer = """
Breast cancer is a malignant tumor arising
from breast tissue and can be treated by
surgery and chemotherapy.
"""

    reference = """
Breast cancer is a malignant disease of breast tissue.
Common treatments include surgery, chemotherapy,
radiotherapy and hormonal therapy.
"""

    results = judge.evaluate(
        question,
        context,
        answer,
        reference
    )

    print("\nLLM Evaluation Results\n")

    for metric, score in results.items():
        print(f"{metric}: {score}%")