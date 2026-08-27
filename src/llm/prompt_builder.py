class PromptBuilder:

    @staticmethod
    def build(question, docs, question_type):

        pdf_context = []
        pubmed_context = []
        kg_context = []

        # -----------------------------
        # Separate evidence by source
        # -----------------------------
        for doc in docs:

            source = doc.get("source", "")

            if source in ["Qdrant", "BM25"]:

                pdf_context.append(
                    f"""
Source : {source}
Page   : {doc.get('page', '-')}

{doc['text']}
"""
                )

            elif source == "PubMed":

                pubmed_context.append(
                    f"""
{doc['text']}
"""
                )

            elif source == "Knowledge Graph":

                kg_context.append(
                    doc["text"]
                )

        prompt = f"""
====================================================
ONCOLOGY QUESTION
====================================================

Question:
{question}

Question Type:
{question_type}

====================================================
TEXTBOOK EVIDENCE
====================================================

{chr(10).join(pdf_context)}

====================================================
PUBMED EVIDENCE
====================================================

{chr(10).join(pubmed_context)}

====================================================
KNOWLEDGE GRAPH FACTS
====================================================

{chr(10).join(kg_context)}

====================================================
INSTRUCTIONS
====================================================

You are an expert Oncology AI Assistant.

Use ONLY the evidence provided.

Answer in the following format.

1. Clinical Summary

2. Explanation

3. Important Medical Concepts

4. Latest Research (if PubMed evidence exists)

5. Knowledge Graph Insights

6. References

If the evidence is insufficient,
explicitly state:

"Insufficient evidence available."

Never hallucinate.

Never invent facts.

Mention page numbers whenever available.
"""

        return prompt