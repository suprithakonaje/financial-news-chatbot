# Financial News Summarizer

## Overview
This is a Retrieval-Augmented Generation (RAG) system designed to provide concise and detailed summaries of news articles. The application retrieves relevant information from a local knowledge base and uses a HuggingFace's language model to generate moderately accurate and context-aware summaries.

## Features
- Load financial news from `data/stock_news.json`.
- Create embeddings with `sentence-transformers/all-MiniLM-L6-v2`.
- Store/retrieve vectors efficiently using FAISS.
- Generate concise answers using `flan-t5-small` (Hugging Face pipeline).
- Simple **Flask-based web UI** to interact with the chatbot.

## Project Structure
The project is organized into the following key directories:

- `src/`: Contains all the source code for the application.
  - `backend/`: Houses the core RAG logic.
    - `rag_generator.py`: Manages the generation of summaries.
    - `rag_retriever.py`: Handles the retrieval of data from the knowledge base.

  - `frontend/`: Contains the web interface and server-side logic.
    - `app.py`: The main application entry point.
    - `templates/`: Stores the HTML files for the web interface.
  - `evaluate_model/`: Evaluate the model with BERTScore and ROGUE
- `data/`: Stores the raw data, such as stock_news.json.
- `tests/`: Contains unit tests for the backend logic.
- `requirements.txt`: Lists all the necessary Python dependencies.

## Prerequisites
1. To run this project, you will need to have Python 3 installed on your system and ensure it is added to your PATH variable.
2. Run PowerShell or any other command line as an administrator.

## Installation
Follow these steps to set up the project locally.
1. Clone the repository: 
```
git clone https://github.com/suprithakonaje/financial-news-chatbot.git
```

2. Navigate to the project directory: 
```
cd .\financial-news-chatbot\
```

3. Create and activate a virtual environment: \
It is highly recommended to use a virtual environment to manage dependencies. In your terminal,
```
# For Windows

python -m venv venv
.\venv\Scripts\activate
```
**Check Troubleshoot section, if you are not able to create a virtual environment.**
4. Install the required packages:
```
pip install -r requirements.txt
```

## Usage
1. To run the application, navigate to the project root and execute the main application file.
```
python -m src.frontend.app
```

2. After running the command, it may take time to load. Once, it loads the following 
```
 * Debugger is active!
 * Debugger PIN: 559-148-682
```

3. Open your web browser and navigate to the URL provided in the terminal output (e.g., http://127.0.0.1:5000) to access the chatbot interface.

4. You can choose between two types of news summaries (Example Query: What is the news with Apple?):
   1. Concise – A shorter summary, showing information from the top 2 sources. 
   2. Detailed – A longer summary, showing information from the top 3 sources. 
   3. Feel free to try queries for other companies as well.


## Running Tests
To run the test suite, ensure your virtual environment is activated and run the following commands from the project root: 
````
(In powershell)
    $env:PYTHONPATH = "."
    pytest -v

(In Command Prompt)
    set PYTHONPATH=.
    pytest -v

````

## Evaluation
ROUGE and BERTScore are used to measure the quality of generated summaries metrics on a subset of the dataset. These metrics provide insights into how closely the generated summaries match reference summaries.

**How to run evaluation script:**
1. Make sure your virtual environment is activated.
2. Run the evaluation script:
    `````
    python -m src.evaluate_model
    `````

**Interpretation**:
1. For queries with well-aligned references (e.g., Amazon), both ROUGE and BERTScore are strong.
2. For noisier topics (e.g., Apple AI), ROUGE scores are lower due to wording drift and extra details pulled in by RAG, though BERTScore indicates the summaries remain semantically similar.


## Troubleshoot
1. After installing Python, if you are unable to create a virtual environment, follow these steps:
2. Check your Python version by running: 
   ```
   python --version
   ```
    It should show version as `Python 3.XX.X`

3. Make sure your username or file path does not contain any whitespace. If it does, clone the repository in a path without spaces.
3. In the terminal, run the following command to temporarily allow script execution:
    ```
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ``` 
    When prompted, type Y and press Enter.
4. Now, try activating your virtual environment:
    ```
   .\venv\Scripts\Activate.ps1
   ```

## Observations & Potential Improvements
1. The system performs well on queries where the retrieved news is highly aligned with the reference (e.g., Amazon shopping feed update). In such cases, both ROUGE and BERTScore scores are strong, reflecting accurate and semantically faithful summaries.
2. For broader or noisier queries (e.g., Apple AI initiatives), the summarizer tends to include extra details from multiple sources. This leads to low ROUGE scores (less lexical overlap with reference summaries) but still high BERTScore, showing that the output is semantically meaningful though phrased differently
3. The RAG system works efficiently for a small to medium-sized dataset, but performance may degrade with very large news corpora.
4. FAISS indexing currently uses `IndexFlatL2`. For larger datasets, consider using `IndexIVFFlat` or `HNSW` for faster retrieval.
5. The system currently uses a small model (`flan-t5-small`). Upgrading to a larger model could improve summary quality.
6. Error handling for edge cases (empty queries, unavailable sources) can be enhanced.
7. Adding caching for generated summaries could improve repeated query performance.

## Limitations
1. Summaries may include minor inaccuracies since LLMs may hallucinate.
2. Currently only supports English-language financial news.
3. The knowledge base is static (no live update of news).

## Next Steps / Contributions
1. Integrate real-time news API for live updates.
2. Improve multi-company queries and context handling.
3. Optimize FAISS index for larger datasets.
4. Explore fine-tuning or using larger summarization models for improved accuracy.
5. Extend language support beyond English to broaden applicability.
