# Private AI Search Engine for Local Documents

This project is a full-stack, containerized application that allows you to run a powerful AI search engine on your local machine. You can ask questions in natural language about your PDF, DOCX, and TXT files and receive accurate, source-cited answers from a local Large Language Model (LLM).

The entire application stack—including the FastAPI backend, the React frontend, and the Ollama LLM server—is managed by Docker, enabling a simple, one-command setup on any machine.

## Key Features

-   **Semantic Search:** Ask questions like "What were our Q4 earnings?" instead of typing keywords.
-   **100% Local & Private:** All files, services, and AI models run in containers on your machine. No data ever leaves your computer.
-   **Source-Cited Answers:** The AI-generated answers include citations to the original source documents, so you can verify the information.
-   **Dynamic Indexing:** The UI allows you to point the engine at any directory on your computer and re-index its contents on the fly.
-   **Multi-Format Support:** Ingests and understands `.pdf`, `.docx`, and `.txt` files.
-   **One-Command Setup:** The entire multi-service application is orchestrated with Docker Compose for a true zero-dependency setup (besides Docker itself).

## Architecture

The application is built with a decoupled frontend-backend architecture, fully containerized for portability and consistency. The frontend's Nginx server acts as a **reverse proxy**, securely and efficiently routing API requests to the backend service.

-   **`backend` Service (FastAPI):** A Python container serving a RESTful API. It handles data ingestion, indexing (using Sentence Transformers and FAISS), and the full RAG pipeline for answer generation.
-   **`frontend` Service (React + Nginx):** A lightweight Nginx container serving the static files of the compiled React application. It provides the UI and forwards API calls to the backend.
-   **`ollama` Service:** The official Ollama container, which downloads and serves the LLMs, providing AI inference capabilities to the backend.

## Tech Stack

-   **Orchestration:** Docker, Docker Compose
-   **Backend:** Python, FastAPI, Pydantic, Uvicorn
-   **AI / RAG Pipeline:** Ollama, Sentence Transformers, FAISS
-   **Frontend:** React.js, JavaScript, HTML/CSS, Nginx
-   **Core Libraries:** `pydantic-settings`, `PyMuPDF`
-   **Development:** Git, `npm`, Python `venv`

## Getting Started

### Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
-   Git for cloning the repository.
-   *(Optional for GPU)* An NVIDIA GPU with the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

### Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Couri3r/RAG-Local-Search-Engine.git
    cd RAG-Local-Search-Engine
    ```

2.  **(Optional) Configure the Model:**
    You can change the default LLM by editing the `LLM_MODEL_NAME` environment variable in the `docker-compose.yml` file.

    ⚠️ **Important Note**  
    The LLM model name is **hardcoded** as `llama3.2:3b` in `qa_system.py`.  
    If you are running a different model, the application **will not work** unless you update the code to match your model name.  
    Please take this into consideration before running the app.


4.  **Build and Run the Application:**
    This single command will build the images, create the network, and start all services.
    ```bash
    docker compose up --build
    ```
    The first time you run this, it will take several minutes to download the base images and build your application containers. Subsequent startups will be much faster due to caching.

### 4. Place Your Files in the Search Directory

**This is a critical step.** Because the application runs inside a container, it can only see files in directories that are explicitly shared with it.

-   In the main project folder, you will find a directory named `documents`. (If it's not there you can just create it yourself).
-   **Copy any files or folders** you want to search into this `documents` directory.
-   The application can only see and index content placed inside this folder.
-   After having everything you need in the `documents` directory, just type `/documents` into the box and hit re-inedx.

5.  **Download an LLM Model:**
    The Ollama container starts empty. Open a **new, separate terminal** and use the `docker exec` command to pull your desired model into the running container.
    ```bash
    # Find your container's name first
    docker ps

    # Use the name to pull a model (e.g., gemma:2b)
    docker exec -it <your-ollama-container-name> ollama pull gemma:2b
    ```
    You only need to do this once. The model will be persisted in a Docker volume.

6.  **Access the Application:**
    Open your web browser and navigate to:
    **`http://localhost:3000`**

7.  **First Use:**
    Use the sidebar to enter `/documents` to index, then click "Re-index". Once the indexing is complete, you can start asking questions!

### How to Stop the Application

-   To stop all running services, go to the terminal where you ran `docker compose up` and press **`CTRL+C`**.
-   To remove the containers and the network entirely, you can run `docker compose down`.
