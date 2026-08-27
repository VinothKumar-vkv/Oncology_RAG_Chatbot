class ContextFusion:

    def merge(self, pdf_docs, pubmed_docs, kg_docs):

        merged = []

        # ---------------- PDF Documents ----------------

        for doc in pdf_docs:

            merged.append({
                "source": doc.get("source", "PDF"),
                "page": doc.get("page", "-"),
                "score": doc.get("score", 0),
                "text": doc.get("text", "")
            })

        # ---------------- PubMed ----------------

        for paper in pubmed_docs:

            merged.append({
                "source": "PubMed",
                "page": "N/A",
                "score": 0,
                "text": f"{paper.get('title', '')}\n\n{paper.get('abstract', '')}"
            })

        # ---------------- Knowledge Graph ----------------

        for fact in kg_docs:

            if isinstance(fact, dict):

                merged.append({
                    "source": fact.get("source", "Knowledge Graph"),
                    "page": fact.get("page", "Graph"),
                    "score": fact.get("score", 1.0),
                    "text": fact.get("text", "")
                })

            else:

                merged.append({
                    "source": "Knowledge Graph",
                    "page": "Graph",
                    "score": 1.0,
                    "text": str(fact)
                })

        return merged