import spacy


class MedicalEntityExtractor:

    def __init__(self):

        print("Loading SciSpacy model...")

        self.nlp = spacy.load("en_core_sci_sm")

    def extract(self, text):

        doc = self.nlp(text)

        entities = []

        seen = set()

        for ent in doc.ents:

            name = ent.text.strip()

            if len(name) < 2:
                continue

            if name.lower() in seen:
                continue

            seen.add(name.lower())

            entities.append(name)

        return entities


if __name__ == "__main__":

    extractor = MedicalEntityExtractor()

    question = input("Question: ")

    entities = extractor.extract(question)

    print("\nExtracted Entities\n")

    for entity in entities:
        print(entity)