class RelationshipValidator:

    def __init__(self):

        # Allowed source_type -> relation -> target_type

        self.rules = {

            "Cancer": {

                "TREATED_WITH": ["Drug", "Treatment"],

                "HAS_GENE": ["Gene"],

                "HAS_BIOMARKER": ["Biomarker"],

                "DIAGNOSED_BY": ["Procedure"],

                "METASTASIZES_TO": ["Organ"],

                "ASSOCIATED_WITH": [
                    "Disease",
                    "Symptom",
                    "Gene",
                    "Biomarker"
                ],

                "EXPRESSES": ["Protein"],

                "OVEREXPRESSES": ["Protein"],

                "RESPONDS_TO": ["Drug"],

                "RESISTANT_TO": ["Drug"],

                "PREVENTED_BY": ["Treatment"]
            },

            "Disease": {

                "TREATED_WITH": ["Drug", "Treatment"],

                "HAS_GENE": ["Gene"],

                "DIAGNOSED_BY": ["Procedure"],

                "ASSOCIATED_WITH": [
                    "Disease",
                    "Symptom",
                    "Gene"
                ]
            },

            "Gene": {

                "INCREASES_RISK_OF": [
                    "Cancer",
                    "Disease"
                ],

                "CAUSES": [
                    "Disease",
                    "Cancer"
                ]
            },

            "Drug": {

                "TARGETS": [
                    "Protein",
                    "Gene"
                ]
            }
        }

    def is_valid(

        self,

        source_type,

        relation,

        target_type

    ):

        if source_type not in self.rules:

            return False

        if relation not in self.rules[source_type]:

            return False

        return target_type in self.rules[source_type][relation]


if __name__ == "__main__":

    validator = RelationshipValidator()

    print(

        validator.is_valid(

            "Cancer",

            "TREATED_WITH",

            "Drug"

        )

    )

    print(

        validator.is_valid(

            "Cancer",

            "AFFECTS",

            "Protein"

        )

    )