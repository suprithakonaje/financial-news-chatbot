import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import faiss
from sentence_transformers import SentenceTransformer as st

BASE = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE / "data"
CACHE_DIR = BASE / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 64


class Retriever:
    """
        Handles loading financial news data, embedding it, building a FAISS index,
        and retrieving the most relevant documents for a query.
    """
    def __init__(self, filepath: str = None):
        self.data_path = Path(filepath) if filepath else DATA_DIR / "stock_news.json"
        self.reports: List[Dict[str, Any]] = []
        self.texts: List[str] = []
        self.embedding_model = st(EMBEDDING_MODEL_NAME)

        self.load_transform_data()
        self.build_faiss_index()

    def load_transform_data(self):
        """
            Loads JSON data from file and normalizes into a flat list of reports
            with ticker, title, link, and full_text fields.
        """
        print("Loading data from:", self.data_path.resolve())
        try:
            with open(self.data_path, 'r', encoding="utf-8") as f:
                raw_data = json.load(f)
        except FileNotFoundError:
            print(
                f"Error: The file '{self.data_path}' was not found. Please ensure it's in the same directory as this script.")
            exit()

        transformed_data = []

        if isinstance(raw_data, dict):
            for ticker, items in raw_data.items():
                if not isinstance(items, list):
                    continue

                for item in items:
                    title = item.get("title", "")
                    link = item.get("link", "")
                    full_text = item.get("full_text", "")
                    transformed_data.append({"ticker": ticker, "title": title, "link": link, "full_text": full_text})
        elif isinstance(raw_data, list):
            for data in raw_data:
                transformed_data.append({
                    "ticker": data.get("ticker", ""),
                    "title": data.get("title", ""),
                    "link": data.get("link", ""),
                    "full_text": data.get("full_text", "")
                })
        else:
            raise ValueError("Unsupported JSON format")

        self.reports = [a for a in transformed_data if a.get("full_text")]
        self.texts = [f"{a.get('title', '')}\n\n{a.get('full_text', '')}" for a in self.reports]

    def cache_paths(self):
        """
            Returns cache file paths for embeddings and FAISS index.
        """
        cache_name = self.data_path.stem
        return {
            "embedding_npy": CACHE_DIR / f"{cache_name}_embeddings.npy",
            "faiss_index": CACHE_DIR / f"{cache_name}_faiss.index",
        }

    def build_faiss_index(self):
        """
            Loads FAISS index from cache if available; otherwise builds a new one.
        """
        cache_paths = self.cache_paths()
        if cache_paths["embedding_npy"].exists() and cache_paths["faiss_index"].exists():
            print("Loading cached embeddings and index")
            self.embeddings = np.load(cache_paths["embedding_npy"])
            self.index = faiss.read_index(str(cache_paths["faiss_index"]))
        else:
            print("No cached files found. Building new index")
            self.compute_embeddings(cache_paths)
            self.build_faiss(cache_paths)

        self.dimension = self.embeddings.shape[1]

    def compute_embeddings(self, cache_paths):
        """
            Computes sentence embeddings for all texts and saves them to cache.
        """
        print("Computing embeddings (may take time on first run)")
        all_embeddings = []
        for i in range(0, len(self.texts), BATCH_SIZE):
            batch = self.texts[i: i + BATCH_SIZE]
            embs = self.embedding_model.encode(batch, convert_to_numpy=True, show_progress_bar=False)
            all_embeddings.append(embs)
        self.embeddings = np.vstack(all_embeddings).astype("float32")
        np.save(cache_paths["embedding_npy"], self.embeddings)
        print("Embeddings saved to cache")

    def build_faiss(self, paths):
        """
            Builds a FAISS index for similarity search and saves it.
        """
        print("Building FAISS index")
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)
        faiss.write_index(self.index, str(paths["faiss_index"]))

    def retrieve(self, query: str, top_k: int = 3, mode: str = "concise") -> List[Dict[str, Any]]:
        """
            Retrieves top_k most relevant reports for the given query.
            Returns metadata including title, link, ticker, and snippet.
        """
        if not query or not hasattr(self, "index"):
            return []

        q_emb = self.embedding_model.encode([query], convert_to_numpy=True).astype("float32")
        distances, indices = self.index.search(q_emb, top_k)

        results = []

        # Normalize query for cosine similarity
        q_norm = q_emb / (np.linalg.norm(q_emb) + 1e-12)

        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.reports):
                continue

            doc_emb = self.embeddings[idx]
            doc_norm = doc_emb / (np.linalg.norm(doc_emb) + 1e-12)

            cosine = float(np.dot(q_norm, doc_norm.T).squeeze())

            report = self.reports[idx]
            snippet = report["full_text"][:600]
            results.append({
                "title": report.get("title", ""),
                "link": report.get("link", ""),
                "ticker": report.get("ticker", ""),
                "snippet": snippet,
                "index": int(idx),
                "score": cosine
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        # Filter results based on mode
        if mode == "concise":
            # Keep only top 2 highest similarity docs for concise summary
            results = [r for r in results if r["score"] > 0.4][:2]
        elif mode == "detailed":
            # Keep more documents (up to top_k)
            results = [r for r in results if r["score"] > 0.1 and len(r["snippet"]) > 50][:top_k]

        return results
