# Private AI Search Engine for Local Documents

This project is a full-stack, containerized application that allows you to run a private, powerful AI search engine on your local machine. Instead of searching by keywords, you can ask questions in natural language about the content of your PDF, DOCX, and TXT files and receive accurate, source-cited answers from a local Large Language Model (LLM).

The entire application stack—including the FastAPI backend, the React frontend, and the Ollama LLM server—is managed by Docker, enabling a simple, one-command setup on any machine.

### Key Features

-   **Semantic Search:** Ask questions like "What were our Q4 earnings?" instead of typing keywords.
-   **100% Local & Private:** All files, services, and AI models run in containers on your machine. No data ever leaves your computer.
-   **Source-Cited Answers:** The AI-generated answers include citations to the original source documents, so you can verify the information.
-   **Dynamic Indexing:** An interactive UI allows you to point the engine at a pre-configured local directory and re-index its contents on the fly.
-   **Multi-Format Support:** Ingests and understands `.pdf`, `.docx`, and `.txt` files.
-   **One-Command Setup:** The entire multi-service application is orchestrated with Docker Compose.

### Architecture

The application is built with a decoupled frontend-backend architecture, fully containerized for portability and consistency. The frontend's Nginx server acts as a **reverse proxy**, securely and efficiently routing API requests to the backend service.

-   **`backend` Service (FastAPI):** A Python container serving a RESTful API. It handles data ingestion, indexing (using Sentence Transformers and FAISS), and the full RAG pipeline for answer generation.
-   **`frontend` Service (React + Nginx):** A lightweight Nginx container serving the static files of the compiled React application. It provides the UI and forwards API calls to the backend.
-   **`ollama` Service:** The official Ollama container, which downloads and serves the LLMs, providing AI inference capabilities to the backend.

### Tech Stack

-   **Orchestration:** Docker, Docker Compose
-   **Backend:** Python, FastAPI, Pydantic, Uvicorn
-   **AI / RAG Pipeline:** Ollama, Sentence Transformers, FAISS
-   **Frontend:** React.js, JavaScript, HTML/CSS, Nginx
-   **Core Libraries:** `pydantic-settings`, `PyMuPDF`
-   **Development:** Git, `npm`, Python `venv`

---

## Getting Started

### Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
-   Git for cloning the repository.

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Couri3r/RAG-Local-Search-Engine.git
    cd RAG-Local-Search-Engine
    ```

2.  **Place Your Files in the Search Directory:**
    **This is a critical step.** The containerized application can only see files in a pre-configured shared directory.
    -   In the main project folder, create a directory named `documents`.
    -   **Copy any files or folders** you want to search into this `documents` directory.

3.  **Build and Run the Application:**
    This single command will build the images, create the network, and start all services.
    ```bash
    docker compose up --build
    ```
    The first time you run this, it will take **several minutes (potentially 20-30 min)** to download the base images and install all the backend dependencies (like PyTorch). Subsequent startups will be much faster due to Docker's caching.

4.  **Download the Required LLM Model:**
    The application is currently configured to use a specific model. Open a **new, separate terminal** and run the following command to pull this model into the running Ollama container.

    ⚠️ **Important Note:** The code currently has `llama3:8b` (or your chosen model) hardcoded as the LLM. You **must** pull this specific model for the application to work.
    ```bash
    # First, find your container's exact name
    docker ps

    # Use the name from the list to pull the required model
    # Example: docker exec -it llmfilesearch-ollama-1 ollama pull llama3:8b
    docker exec -it <your-ollama-container-name> ollama pull llama3:8b
    ```
    You only need to do this once. The model will be persisted in a Docker volume.

5.  **Access the Application:**
    Open your web browser and navigate to:
    **`http://localhost:3000`**

6.  **Perform Initial Index:**
    -   Use the sidebar and click the "Re-index" button. The input box should be left **blank** to index the entire `documents` folder.
    -   Once indexing is complete, you can start asking questions!

