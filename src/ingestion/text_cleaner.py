import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean extracted PDF text.
        """

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n+", "\n", text)

        # Remove page numbers standing alone
        text = re.sub(r"\b\d+\b", " ", text)

        # Remove repeated spaces again
        text = re.sub(r"\s{2,}", " ", text)

        return text.strip()


if __name__ == "__main__":

    sample = """
    Page 23

    Breast      Cancer

    This     is      a    sample.

    123

    """

    cleaner = TextCleaner()

    print(cleaner.clean(sample))