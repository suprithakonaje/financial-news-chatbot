from src.backend.rag_generator import Generator
from src.backend.rag_retriever import Retriever

from rouge_score import rouge_scorer
import bert_score

# Initialize retriever and generator
retriever = Retriever("data/stock_news.json")
generator = Generator()

# Sample evaluation queries and reference summaries
test_queries = [
    {
        "query": "Apple AI initiatives",
        "concise_ref": "Apple has launched new AI initiatives focusing on machine learning and user experience.",
        "detailed_ref": "Apple has introduced several AI initiatives aimed at improving user experience and integrating machine learning into its products, according to multiple news sources."
    },
    {
        "query": "Amazon shopping feed update",
        "concise_ref": "Amazon is shutting down its Inspire shopping feed inside its mobile app.",
        "detailed_ref": "Amazon.com has decided to close its Inspire shopping feed inside the mobile app, consolidating its shopping features and responding to user engagement patterns."
    }
]

# Initialize ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

print("\n===== Model Evaluation =====\n")

for item in test_queries:
    query = item["query"]

    for mode in ["concise", "detailed"]:
        retrieved_docs = retriever.retrieve(query, top_k=3, mode=mode)
        generated_summary = generator.generate(query, retrieved_docs, mode=mode)
        reference = item[f"{mode}_ref"]

        # Compute ROUGE
        rouge_scores = scorer.score(reference, generated_summary)

        # Compute BERTScore
        P, R, F1 = bert_score.score([generated_summary], [reference], lang="en")

        print(f"Query: {query} | Mode: {mode}")
        print(f"Generated: {generated_summary}")
        print(f"Reference: {reference}")
        print("ROUGE-1: {:.2f}, ROUGE-2: {:.2f}, ROUGE-L: {:.2f}".format(
            rouge_scores['rouge1'].fmeasure,
            rouge_scores['rouge2'].fmeasure,
            rouge_scores['rougeL'].fmeasure
        ))
        print("BERTScore F1: {:.2f}".format(F1[0].item()))
        print("-" * 80)
