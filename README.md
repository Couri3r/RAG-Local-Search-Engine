This project is a full-stack application that allows you to run a private, powerful AI search engine on your local machine. Instead of searching by keywords, you can ask questions in natural language about the content of your PDF, DOCX, and TXT files. The system uses a Retrieval-Augmented Generation (RAG) pipeline to find the most relevant information and generate a coherent, source-cited answer using a local Large Language Model (LLM).

## Key Features

-   **Semantic Search:** Ask questions like "What were our Q4 earnings?" instead of typing keywords.
-   **Local & Private:** All your files and the AI model run 100% on your machine. No data is ever sent to the cloud.
-   **Source-Cited Answers:** The AI-generated answers include citations to the original source documents, so you can verify the information.
-   **Dynamic Indexing:** An interactive UI allows you to point the engine at any directory on your computer and re-index its contents on the fly.
-   **Multi-Format Support:** Ingests and understands `.pdf`, `.docx`, and `.txt` files.
-   **Modern Tech Stack:** Built with a FastAPI backend and a responsive React frontend.

## Architecture

The application is built with a clean, decoupled frontend-backend architecture.

-   **Backend (FastAPI):** A Python-based server that exposes a RESTful API. It handles:
    -   **Data Ingestion:** Processing and extracting text from various file formats.
    -   **Indexing:** Creating vector embeddings using Sentence Transformers (BGE) and storing them in a FAISS vector index.
    -   **Retrieval & Generation:** Receiving a query, searching the FAISS index for relevant context, and using a local LLM
 
⚠️ Important Note:
The code currently has llama3.2:3b hardcoded as the LLM model. The application will not work if you are running a different model. Please take this into consideration.

-   **Frontend (React):** A modern, single-page application that provides the user interface. It:
    -   Communicates with the FastAPI backend via API calls.
    -   Displays the list of indexed files, the search bar, and the formatted results.
    -   Allows the user to dynamically trigger the re-indexing of new directories.

## Tech Stack

-   **Backend:** Python, FastAPI, Pydantic, Uvicorn
-   **AI / RAG Pipeline:** Ollama, Sentence Transformers, FAISS, LangChain
-   **Frontend:** React.js, JavaScript, HTML/CSS
-   **Core Libraries:** `pydantic-settings`, `python-dotenv`, `PyMuPDF`
-   **Development:** Git, npm, Python venv

## Setup and Installation

### Prerequisites

-   Python 3.9+
-   Node.js and npm
-   [Ollama](https://ollama.com/) installed and running.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Couri3r/RAG-Local-Search-Engine.git
    ```

2.  **Setup the Backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Setup the Frontend:**
    ```bash
    cd ../frontend
    npm install
    ```

## How to Run

You will need two terminals running simultaneously.

1.  **Run the Backend Server:**
    -   Make sure Ollama is running.
    -   Pull a model, e.g., `ollama pull gemma:2b`.
    -   In a terminal at the `backend` directory:
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

2.  **Run the Frontend Application:**
    -   In a second terminal at the `frontend` directory:
    ```bash
    npm start
    ```
    The application will open in your browser at `http://localhost:3000`.

3.  **First Use:** Use the UI to point the engine at a directory on your computer and perform the initial indexing. Then, start asking questions!
