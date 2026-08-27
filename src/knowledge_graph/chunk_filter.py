import re


class MedicalChunkFilter:

    def __init__(self):

        self.skip_patterns = [

            r"references",

            r"bibliography",

            r"copyright",

            r"all rights reserved",

            r"isbn",

            r"contents",

            r"table of contents",

            r"index",

            r"acknowledgements",

            r"preface"

        ]

        self.medical_keywords = [

            "cancer",
            "tumor",
            "tumour",
            "oncology",
            "carcinoma",
            "therapy",
            "chemotherapy",
            "radiotherapy",
            "drug",
            "gene",
            "mutation",
            "protein",
            "biomarker",
            "metastasis",
            "diagnosis",
            "treatment",
            "survival",
            "breast",
            "lung",
            "colon",
            "melanoma",
            "leukemia",
            "lymphoma",
            "her2",
            "brca",
            "tp53"

        ]

    def should_process(self, text):

        text_lower = text.lower()

        # Skip unwanted pages
        for pattern in self.skip_patterns:

            if re.search(pattern, text_lower):

                return False

        # Keep only medical chunks
        for keyword in self.medical_keywords:

            if keyword in text_lower:

                return True

        return False


if __name__ == "__main__":

    filter = MedicalChunkFilter()

    sample1 = "Breast cancer is treated using trastuzumab."

    sample2 = "References"

    print(filter.should_process(sample1))

    print(filter.should_process(sample2))