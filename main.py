from src.backend.rag_retriever import Retriever
from src.backend.rag_generator import Generator

def main():
    try:
        retriever = Retriever()
        generator = Generator()

        print("Financial News Chatbot (CLI)")
        print("You can ask about company news, stock updates, etc.")
        print("Type 'exit' or 'quit' to leave.\n")

        # Choose response mode
        modes = {"1": "concise", "2": "detailed"}
        print("Choose response mode:")
        print("1: Concise")
        print("2: Detailed")
        mode_choice = input("Enter 1 or 2 (default 1): ").strip()
        mode = modes.get(mode_choice, "concise")
        print(f"\nMode selected: {mode}\n")

        while True:
            user_query = input("You: ").strip()
            if user_query.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not user_query:
                print("Query cannot be empty.\n")
                continue

            retrieved_docs = retriever.retrieve(user_query, top_k=3, mode=mode)

            if not retrieved_docs:
                print("Bot: Sorry, I couldn't find relevant news.\n")
                continue

            summary = generator.generate(user_query, retrieved_docs, mode=mode)
            print(f"\nBot ({mode}): {summary}\n")

            # Show sources
            print("Sources:")
            for idx, article in enumerate(retrieved_docs, start=1):
                print(f"[{idx}] {article.get('title', 'No title')} - {article.get('link', '#')}")
            print("-" * 60)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have all dependencies installed and the 'stock_news.json' file is in the correct location.")

if __name__ == "__main__":
    main()
