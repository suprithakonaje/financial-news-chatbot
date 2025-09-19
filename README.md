# Financial News Summarizer

## Overview
This is a Retrieval-Augmented Generation (RAG) system designed to provide concise summaries of news articles. The application retrieves relevant information from a local knowledge base and uses a language model to generate accurate and context-aware summaries.

## Features
- Load financial news from `data/stock_news.json`.
- Create embeddings with `sentence-transformers/all-MiniLM-L6-v2`.
- Store/retrieve vectors efficiently using FAISS.
- Generate concise answers using `flan-t5-small` (Hugging Face pipeline).
- Simple **Flask-based web UI** to interact with the chatbot.

## Prerequisites
To run this project, you will need to have Python3 installed on your system.

## Installation
Follow these steps to set up the project locally.
1. Clone the repository: 
```
git clone [https://github.com/your-username/NewsSummariser.git](https://github.com/your-username/NewsSummariser.git)
```

2. Navigate to the project directory: 
```
cd NewsSummariser
```

3. Create and activate a virtual environment: \
It is highly recommended to use a virtual environment to manage dependencies. 
```
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```
4. Install the required packages:
```
pip install -r requirements.txt
```

## Usage
To run the application, navigate to the project root and execute the main application file.
```
python -m src.frontend.app
```

After running the command, the application should start a local web server. Open your web browser and navigate to the URL provided in the terminal output (e.g., http://127.0.0.1:5000) to access the chatbot interface.

## Project Structure
The project is organized into the following key directories:

- `src/`: Contains all the source code for the application.
  - `backend/`: Houses the core RAG logic.
    - `rag_generator.py`: Manages the generation of summaries.
    - `rag_retriever.py`: Handles the retrieval of data from the knowledge base.

  - `frontend/`: Contains the web interface and server-side logic.
    - `app.py`: The main application entry point.
    - `templates/`: Stores the HTML files for the web interface.
- `data/`: Stores the raw data, such as stock_news.json.
- `tests/`: Contains unit tests for the backend logic.
- `requirements.txt`: Lists all the necessary Python dependencies.

## Running Tests
To run the test suite, ensure your virtual environment is activated and run the following command from the project root: 
```
pytest
```
