from langchain_text_splitters import RecursiveCharacterTextSplitter


class MedicalChunker:

    def __init__(
        self,
        chunk_size=800,
        chunk_overlap=150
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split(self, text):

        return self.splitter.split_text(text)


if __name__ == "__main__":

    sample = """
    Breast cancer is one of the most common malignancies.

    Surgery remains the primary treatment.

    Chemotherapy may be required.

    Radiation therapy reduces recurrence.

    Immunotherapy is rapidly evolving.
    """ * 50

    chunker = MedicalChunker()

    chunks = chunker.split(sample)

    print(f"Chunks : {len(chunks)}")

    print()

    print(chunks[0])