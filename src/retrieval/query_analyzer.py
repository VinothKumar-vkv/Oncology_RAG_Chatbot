import re


class MedicalQueryAnalyzer:

    def classify(self, question):

        q = question.lower().strip()

        # ---------------------------------------
        # Clinical Case
        # ---------------------------------------
        if any(word in q for word in [
            "patient",
            "woman",
            "man",
            "child",
            "history",
            "presents",
            "comes",
            "case"
        ]):
            return "clinical_case"

        # ---------------------------------------
        # Definition
        # ---------------------------------------
        if any(word in q for word in [
            "what is",
            "what is meant by",
            "define",
            "meaning of",
            "explain"
        ]):
            return "definition"

        # ---------------------------------------
        # Symptoms
        # ---------------------------------------
        if any(word in q for word in [
            "symptom",
            "sign",
            "presentation",
            "complaint"
        ]):
            return "symptoms"

        # ---------------------------------------
        # Diagnosis
        # ---------------------------------------
        if any(word in q for word in [
            "diagnosis",
            "diagnose",
            "diagnostic",
            "investigation"
        ]):
            return "diagnosis"

        # ---------------------------------------
        # Treatment
        # ---------------------------------------
        if any(word in q for word in [
            "treatment",
            "therapy",
            "management",
            "treat",
            "drug",
            "medication",
            "immunotherapy",
            "targeted therapy",
            "chemotherapy",
            "radiotherapy",
            "surgery"
        ]):
            return "treatment"

        # ---------------------------------------
        # Histopathology
        # ---------------------------------------
        if any(word in q for word in [
            "biopsy",
            "histology",
            "histopathology",
            "microscopy",
            "pathology"
        ]):
            return "histopathology"

        # ---------------------------------------
        # Genetics
        # ---------------------------------------
        if any(word in q for word in [
            "gene",
            "mutation",
            "brca",
            "her2",
            "egfr",
            "alk",
            "genetic"
        ]):
            return "genetics"

        # ---------------------------------------
        # Prognosis
        # ---------------------------------------
        if any(word in q for word in [
            "survival",
            "prognosis",
            "outcome"
        ]):
            return "prognosis"

        # ---------------------------------------
        # Prevention
        # ---------------------------------------
        if any(word in q for word in [
            "prevent",
            "prevention",
            "screening",
            "vaccination"
        ]):
            return "prevention"

        # ---------------------------------------
        # Latest Research
        # ---------------------------------------
        if any(word in q for word in [
            "latest",
            "recent",
            "new",
            "current",
            "2024",
            "2025",
            "2026",
            "clinical trial"
            "journal",
            "paper",
            "publication",
            "meta analysis",
            "systematic review",
            "guideline",
            "nccn",
            "asco",
            "esm"
        ]):
            return "latest_research"

        return "general"


if __name__ == "__main__":

    analyzer = MedicalQueryAnalyzer()

    while True:

        question = input("Question : ")

        print("\nCategory :", analyzer.classify(question))