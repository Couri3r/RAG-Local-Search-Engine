import os
import faiss
import pickle
import ollama
from sentence_transformers import SentenceTransformer

DATA_DIR = "/data"
INDEX_PATH = os.path.join(DATA_DIR, "faiss_index.bin")
METADATA_PATH = os.path.join(DATA_DIR, "metadata.pkl")
MODEL_NAME = "BAAI/bge-small-en-v1.5" 
LLM_MODEL_NAME = "llama3.2:3b"     


class RAGSystem:
    def __init__(self):
        print("Starting RAG system")

        self.index = None
        self.metadata = []
        self.embedding_model = None

        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            try:
                print("Found existing index files. Loading...")
                self.index = faiss.read_index(INDEX_PATH)

                with open(METADATA_PATH, "rb") as f:
                    self.metadata = pickle.load(f)
                    print (f"FAISS index and metadata loaded successfully with {len(self.metadata)} chunks.")

            except Exception as e:
                print(f"Error loading existing index files: {e}")

                self.index = None
                self.metadata = []

        else:
            print("No index found. System is starting empty. Please use the re-index endpoint")

        try:

            self.embedding_model = SentenceTransformer(MODEL_NAME)
            print("Sentence transformer model loaded successfully.")

        except Exception as e:
            print("Could not load the sentence transformer model")

        print("Rag system loaded")
    

        
        
        
        
        


    def ask(self,query: str, k: int = 4) -> dict:

        if not query.strip():
            return {"answer": "provide a valid question", "sources": []}

        print(f"\nRecieved Query: {query}") 

        print("Embedding the query")  

        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)   

        query_embedding = query_embedding.astype('float32')    

        print(f"Searching the index for top {k} relevant chunks")  

        distance, indices = self.index.search(query_embedding, k)

        retrieved_chunks = [self.metadata[i] for i in indices[0]]

        unique_sources = set()

        context_parts = []

        for chunk in retrieved_chunks:
            source_filename = os.path.basename(chunk['source'])

            unique_sources.add(source_filename)
            context_parts.append(f"Source: {source_filename}\nContent: {chunk['content']}")

        context_string = "\n\n---\n\n".join(context_parts)



        

        prompt = f"""
        You are an expert Question-Answering assistant.
        Your task is to answer the user's question based ONLY on the provided context.
        Do not use any external knowledge.
        If the context does not contain the answer, state that you cannot answer the question with the information provided.
        Cite the source filename for each piece of information you use by adding [Source: filename.ext] at the end of the sentence.

        **VERY IMPORTANT INSTRUCTION:** When you cite a source, you MUST only use the filename. For example, if the context says "Source: /documents/reports/quarterly/report_q4.pdf", you must cite it as "[Source: report_q4.pdf]". Do not include the full path.

        CONTEXT:
        {context_string}

        USER'S QUESTION:
        {query}

        ANSWER:
        """

        print(f"Sending prompt to an LLM Model: {LLM_MODEL_NAME}")

        ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

        client = ollama.Client(host=ollama_host)

        try:
            response = client.chat(
                model = LLM_MODEL_NAME,
                messages=[{'role': 'user', 'content': prompt}]
            )
            answer = response['message']['content']
            print("LLM generated an answer")
        except Exception as e:
            answer = f"Error communicating with model: {e}"
            print(f"ERROR: {answer}")

        return {
            "answer": answer,
            "sources": list(unique_sources)
        }
    

if __name__ == "__main__":

    try:
        rag_system = RAGSystem()
    except Exception:
        print("Failed to load RAG System")

        exit()

    print("Local RAG Search Engine")
    print("Type 'exit' to quit")

    while True:
        user_query = input("\nAsk a question about your documents\n")
        if user_query.lower() == 'exit':
            break

        result = rag_system.ask(user_query)

        print("\nLLM answer:")
        print(result['answer'])

        if result['sources']:
            print("Sources:")
            for source in result['sources']:
                print(f"- {source}")







