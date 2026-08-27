from src.ingestion.metadata import MetadataGenerator
from src.ingestion.pdf_loader import PDFLoader
from src.ingestion.text_cleaner import TextCleaner
from src.ingestion.chunker import MedicalChunker

from src.knowledge_graph.chunk_filter import MedicalChunkFilter
from src.knowledge_graph.graph_builder import GraphBuilder

import json
from pathlib import Path


class OncologyPipeline:

    def __init__(self):

        # PDF Loader
        self.loader = PDFLoader()

        # Medical Text Chunker
        self.chunker = MedicalChunker()

        # Medical Chunk Filter
        self.filter = MedicalChunkFilter()

        # Knowledge Graph Builder
        self.graph_builder = GraphBuilder()

    def process(self):

        documents = self.loader.load_all_pdfs()

        all_chunks = []

        chunk_id = 1

        total_relationships = 0

        for document in documents:

            filename = document["filename"]

            print(f"\nProcessing {filename}")

            for page in document["pages"]:

                page_number = page["page"]

                cleaned_text = TextCleaner.clean(page["text"])

                chunks = self.chunker.split(cleaned_text)

            

                for chunk in chunks:

                    metadata = MetadataGenerator.create(
                        chunk_id=chunk_id,
                        filename=filename,
                        page=page_number,
                        chunk=chunk,
                        chunk_index=len(all_chunks) + 1
                    )

                    all_chunks.append(metadata)

                    # Only build KG for medical chunks
                    if self.filter.should_process(chunk):

                        relationships = self.graph_builder.build(chunk)

                        total_relationships += relationships

                    chunk_id += 1

        self.graph_builder.close()

        print("\n" + "=" * 60)
        print("Knowledge Graph Construction Finished")
        print("=" * 60)

        print(f"Total Chunks           : {len(all_chunks)}")
        print(f"Relationships Inserted : {total_relationships}")

        return all_chunks


if __name__ == "__main__":

    pipeline = OncologyPipeline()

    chunks = pipeline.process()

    Path("outputs").mkdir(exist_ok=True)

    with open(
        "outputs/processed_chunks.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved to outputs/processed_chunks.json")