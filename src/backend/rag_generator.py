from typing import List, Dict
from transformers import pipeline
import re

# Model for local CPU usage
GENERATOR_MODEL = "google/flan-t5-small"


class Generator:
    """
        Uses a text-to-text generation model (Flan-T5) to create concise summaries
        from retrieved news documents.
    """

    def __init__(self):
        self.generator = pipeline("text2text-generation", model=GENERATOR_MODEL, device=-1)

    def clean_snippet(self, snippet: str) -> str:
        """
                Remove common boilerplate subscription/premium text from news snippets.
        """

        if not snippet:
            return ""

        snippet = re.sub(
            r"(PREMIUM Upgrade|A Silver or Gold subscription plan is required|Already have a subscription|"
            r"Continue Reading|View Comments|Sign in|Read this MT Newswires article|Upgrade|subscribe)",
            "",
            snippet,
            flags=re.IGNORECASE
        )

        snippet = " ".join(snippet.split())
        return snippet.strip()

    def generate(self, query: str, retrieved: List[Dict], mode: str = "concise", max_length: int = 500) -> str:
        """
        Generates a summary using the retrieved documents.
        Args:
            query (str): User's question
            retrieved (List[Dict]): Retrieved news documents
            mode (str): "concise" or "detailed"
            max_length (int): Max tokens in generated response

        Returns:
            str: Generated answer text
        """

        context_parts = []

        for index, article in enumerate(retrieved, start=1):
            snippet = self.clean_snippet(article.get("snippet", ""))
            if not snippet:
                continue

            if mode == "detailed":
                title = article.get("title", "")
                part = f"[{index}] {title}: {snippet}"
                context_parts.append(part)
            else:
                context_parts.append(snippet)

        if not context_parts:
            return "Sorry, I couldn't find meaningful news for that query."

        context = "\n\n".join(context_parts)

        if mode == "detailed":
            instruction = (
                "You are a financial news assistant. Using the context below, "
                "write a single, well-structured paragraph in plain English. "
                "Summarize the key facts without repeating text verbatim. "
                "Do not include irrelevant boilerplate like 'Upgrade' or 'premium'. "
                "If multiple sources mention the same news, merge them into one cohesive explanation."
            )
            max_new_tokens  = max_length
            do_sample = True
            top_p = 0.9
            temperature = 0.7
        else:
            instruction = (
                "You are a financial news assistant. Using the context below, "
                "write a **clear and concise one-sentence summary** in proper English. "
                "Focus on the main point only."
            )
            max_new_tokens = 60
            do_sample = False
            top_p = None
            temperature = None

        prompt = f"{instruction}\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"

        out = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            top_p=top_p,
            temperature=temperature,
            truncation=True
        )

        text = out[0]["generated_text"].strip()

        if text.startswith(context):
            text = text[len(context):].strip()

        return text
