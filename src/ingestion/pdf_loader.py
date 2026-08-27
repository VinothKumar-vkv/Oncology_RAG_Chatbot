from pathlib import Path
import fitz


class PDFLoader:

    def __init__(self, pdf_folder="data/pdfs"):
        self.pdf_folder = Path(pdf_folder)

    def load_all_pdfs(self):

        pdf_files = list(self.pdf_folder.glob("*.pdf"))

        if not pdf_files:
            print("No PDF files found.")
            return []

        documents = []

        for pdf in pdf_files:

            print(f"Reading: {pdf.name}")

            doc = fitz.open(pdf)

            pages = []

            for page_number, page in enumerate(doc):

                text = page.get_text()

                pages.append({
                    "page": page_number + 1,
                    "text": text
                })

            documents.append({
                "filename": pdf.name,
                "pages": pages
            })

            doc.close()

        return documents


if __name__ == "__main__":

    loader = PDFLoader()

    docs = loader.load_all_pdfs()

    print("=" * 50)

    print(f"Total PDFs: {len(docs)}")

    if docs:

        print(f"PDF Name : {docs[0]['filename']}")

        print(f"Pages : {len(docs[0]['pages'])}")

        print()

        print(docs[0]["pages"][0]["text"][:1000])