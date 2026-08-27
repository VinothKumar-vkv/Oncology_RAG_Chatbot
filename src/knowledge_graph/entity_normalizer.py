class EntityNormalizer:

    def __init__(self):

        self.mapping = {

            # -------------------------
            # Breast Cancer
            # -------------------------
            "breast cancer": "Breast Cancer",
            "breast carcinoma": "Breast Cancer",
            "mammary carcinoma": "Breast Cancer",
            "her2 positive breast cancer": "Breast Cancer",

            # -------------------------
            # HER2
            # -------------------------
            "her2": "HER2",
            "her2 protein": "HER2",
            "her-2": "HER2",
            "erbb2": "HER2",

            # -------------------------
            # BRCA1
            # -------------------------
            "brca1": "BRCA1",
            "brca1 mutation": "BRCA1",

            # -------------------------
            # Trastuzumab
            # -------------------------
            "trastuzumab": "Trastuzumab",
            "herceptin": "Trastuzumab",

            # -------------------------
            # Tamoxifen
            # -------------------------
            "tamoxifen": "Tamoxifen"
        }

    def normalize(self, entity):

        entity = entity.strip()

        key = entity.lower()

        return self.mapping.get(key, entity)

if __name__ == "__main__":

    normalizer = EntityNormalizer()

    tests = [

        "breast cancer",

        "HER2 Protein",

        "BRCA1 mutation",

        "Herceptin"

    ]

    for t in tests:

        print(t, "->", normalizer.normalize(t))