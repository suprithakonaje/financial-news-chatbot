import pytest
from unittest.mock import patch, MagicMock
from src.backend.rag_generator import Generator

@pytest.fixture
def fake_docs():
    return [
        {"title": "Apple Launch", "ticker": "AAPL", "snippet": "Apple announced a new product."},
        {"title": "Microsoft AI", "ticker": "MSFT", "snippet": "Microsoft backed OpenAI released a model."},
    ]

@pytest.fixture
def mock_pipeline():
    with patch("src.backend.rag_generator.pipeline") as mock_pipe:
        mock_instance = MagicMock()
        # Always return a fixed text for predictability
        mock_instance.return_value = [{"generated_text": "Mocked summary text."}]
        mock_pipe.return_value = mock_instance
        yield mock_pipe

def test_generate_concise(fake_docs, mock_pipeline):
    gen = Generator()
    answer = gen.generate("What is Apple doing?", fake_docs, mode="concise")
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert answer == "Mocked summary text."

def test_generate_detailed(fake_docs, mock_pipeline):
    gen = Generator()
    answer = gen.generate("What is Apple doing?", fake_docs, mode="detailed")
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert answer == "Mocked summary text."
