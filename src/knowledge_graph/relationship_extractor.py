import json

from src.llm.llama_client import LlamaClient


class RelationshipExtractor:

    def __init__(self):

        self.llm = LlamaClient()

    def extract(self, text):

        prompt = f"""
You are an expert Oncology Knowledge Graph Builder.

Extract ONLY meaningful biomedical relationships from the text.

Return ONLY a valid JSON array.

---------------------------------------------------
Allowed Entity Types
---------------------------------------------------

Disease
Cancer
Drug
Gene
Protein
Biomarker
Symptom
Treatment
Procedure
Organ

---------------------------------------------------
Allowed Relationship Types
---------------------------------------------------

TREATED_WITH
HAS_GENE
HAS_BIOMARKER
HAS_MUTATION
CAUSES
ASSOCIATED_WITH
INCREASES_RISK_OF
DIAGNOSED_BY
METASTASIZES_TO
AFFECTS
EXPRESSES
OVEREXPRESSES
TARGETS
RESPONDS_TO
RESISTANT_TO
PREVENTED_BY

---------------------------------------------------
Rules
---------------------------------------------------

1. Extract ONLY specific biomedical entities.

2. Ignore generic words like

Patients
Patient
Disease
Cancer
Genes
Gene
Protein
Proteins
Women
Men
People
Tumor
Cell
Cells
Unknown
Unknown Organ

3. Do NOT invent relationships.

4. If no relationship exists, return exactly

[]

5. Return ONLY JSON.

6. No explanation.

7. No markdown.

8. No notes.

---------------------------------------------------
Example
---------------------------------------------------

[
    {{
        "source":"Breast Cancer",
        "source_type":"Cancer",
        "relation":"HAS_GENE",
        "target":"HER2",
        "target_type":"Gene"
    }},
    {{
        "source":"Breast Cancer",
        "source_type":"Cancer",
        "relation":"TREATED_WITH",
        "target":"Trastuzumab",
        "target_type":"Drug"
    }}
]

---------------------------------------------------
Text
---------------------------------------------------

{text}
"""

        response = self.llm.generate(prompt)

        if response is None:

            print("No response received from LLM.")

            return "[]"

        # -----------------------------
        # Extract only JSON
        # -----------------------------

        start = response.find("[")
        end = response.rfind("]")

        if start == -1 or end == -1:
            return "[]"

        response = response[start:end + 1]

        # -----------------------------
        # Validate JSON
        # -----------------------------

        try:

            triples = json.loads(response)

            return json.dumps(
                triples,
                indent=4,
                ensure_ascii=False
            )

        except Exception:

            return "[]"


if __name__ == "__main__":

    extractor = RelationshipExtractor()

    sample = """
    HER2 positive breast cancer is commonly treated with trastuzumab.

    BRCA1 mutation increases breast cancer risk.

    HER2 protein is overexpressed in HER2 positive breast cancer.

    Tamoxifen is used for hormone receptor positive breast cancer.
    """

    print(extractor.extract(sample))