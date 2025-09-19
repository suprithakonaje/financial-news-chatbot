from src.backend.rag_retriever import Retriever

DATA_PATH = "data/stock_news.json"


def test_retriever_load():
    retriever = Retriever(DATA_PATH)
    # Ensure data loaded
    assert len(retriever.reports) > 0
    # Check embeddings exist
    assert hasattr(retriever, "embeddings")
    assert retriever.embeddings.shape[0] == len(retriever.reports)
    # Check FAISS index exists
    assert hasattr(retriever, "index")


def test_retrieve_concise():
    retriever = Retriever(DATA_PATH)
    results = retriever.retrieve("Apple", top_k=3, mode="concise")
    assert isinstance(results, list)
    # At least one result
    assert len(results) > 0
    # Check keys
    for r in results:
        assert "title" in r
        assert "snippet" in r
        assert "score" in r
        # Score should be between 0 and 1
        assert 0 <= r["score"] <= 1
    # Concise mode should return max 2 results
    assert len(results) <= 2


def test_retrieve_detailed():
    retriever = Retriever(DATA_PATH)
    results = retriever.retrieve("Apple", top_k=3, mode="detailed")
    assert isinstance(results, list)
    # At least one result
    assert len(results) > 0
    # Check keys
    for r in results:
        assert "title" in r
        assert "snippet" in r
        assert "score" in r
        assert 0 <= r["score"] <= 1
        # Detailed mode should include longer snippets
        assert len(r["snippet"]) > 50
    # Detailed mode can return up to top_k results
    assert len(results) <= 3
