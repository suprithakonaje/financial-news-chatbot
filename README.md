# Financial News Summarizer

## Overview
This is a Retrieval-Augmented Generation (RAG) system designed to provide concise and detailed summaries of news articles. The application retrieves relevant information from a local knowledge base and uses a HuggingFace's language model to generate moderately accurate and context-aware summaries.

## Features
- Load financial news from `data/stock_news.json`.
- Create embeddings with `sentence-transformers/all-MiniLM-L6-v2`.
- Store/retrieve vectors efficiently using FAISS.
- Generate concise answers using `flan-t5-small` (Hugging Face pipeline).
- Simple **Flask-based web UI** to interact with the chatbot.

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
To run the test suite, ensure your virtual environment is activated and run the following commands from the project root: 
````
(In powershell)
    $env:PYTHONPATH = "."
    pytest -v

(In Command Prompt)
    set PYTHONPATH=.
    pytest -v

````

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
