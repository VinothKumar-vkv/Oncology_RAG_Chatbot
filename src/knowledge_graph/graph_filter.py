class GraphFilter:

    def __init__(self):

        self.allowed = {

            "definition": [
                "HAS_GENE",
                "ASSOCIATED_WITH"
            ],

            "diagnosis": [
                "DIAGNOSED_BY",
                "HAS_BIOMARKER"
            ],

            "treatment": [
                "TREATED_WITH",
                "RESPONDS_TO",
                "TARGETS",
                "RESISTANT_TO"
            ],

            "genetics": [
                "HAS_GENE",
                "HAS_MUTATION",
                "INCREASES_RISK_OF"
            ],

            "prognosis": [
                "ASSOCIATED_WITH"
            ]
        }

    def filter(self, docs, question_type):

        if question_type not in self.allowed:
            return docs

        relations = self.allowed[question_type]

        filtered = []

        for doc in docs:

            text = doc["text"]

            if any(rel in text for rel in relations):
                filtered.append(doc)

        return filtered