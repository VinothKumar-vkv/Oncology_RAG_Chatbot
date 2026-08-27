import json
import os

from src.knowledge_graph.graph_builder import GraphBuilder
from src.knowledge_graph.chunk_filter import MedicalChunkFilter


CHUNK_FILE = "outputs/processed_chunks.json"
CHECKPOINT_FILE = "outputs/kg_checkpoint.txt"


def load_chunks():
    with open(CHUNK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def save_checkpoint(index):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(index))


def build_knowledge_graph():

    print("=" * 60)
    print("Building Oncology Knowledge Graph")
    print("=" * 60)

    builder = GraphBuilder()
    filter_model = MedicalChunkFilter()

    chunks = load_chunks()

    total_chunks = len(chunks)
    start_index = load_checkpoint()

    print(f"\nTotal Chunks      : {total_chunks}")
    print(f"Starting From     : {start_index}\n")

    processed = 0
    inserted = 0
    skipped = 0

    # Keep track of the latest processed chunk
    last_processed = start_index

    try:

        for i in range(start_index, total_chunks):

            chunk = chunks[i]

            text = chunk.get("text", "").strip()

            if not text:
                skipped += 1
                last_processed = i
                continue

            # Skip non-medical chunks
            if not filter_model.should_process(text):
                skipped += 1
                last_processed = i
                continue

            try:

                builder.build(text)

                inserted += 1
                processed += 1
                last_processed = i

            except Exception as e:

                print(f"\nChunk {i} failed")
                print(e)

                last_processed = i

            # Save checkpoint every 20 processed chunks
            if processed > 0 and processed % 20 == 0:

                save_checkpoint(last_processed)

                print(
                    f"[{last_processed}/{total_chunks}] "
                    f"Inserted={inserted} "
                    f"Skipped={skipped}"
                )

    except KeyboardInterrupt:

        print("\n\nInterrupted by user.")

        save_checkpoint(last_processed)

    finally:

        builder.close()

    print("\n" + "=" * 60)
    print("Knowledge Graph Build Complete")
    print("=" * 60)

    print(f"Processed : {processed}")
    print(f"Inserted  : {inserted}")
    print(f"Skipped   : {skipped}")

    # Save completion ONLY if every chunk has been processed
    if last_processed >= total_chunks - 1:
        save_checkpoint(total_chunks)
    else:
        save_checkpoint(last_processed)


if __name__ == "__main__":

    build_knowledge_graph()