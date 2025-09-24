import os
import faiss
import pickle
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from .file_processor import process_directory


MODEL_NAME = "BAAI/bge-small-en-v1.5"

CHUNK_SIZE = 600
CHUNK_OVERLAP = 75

import os

BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
METADATA_PATH = os.path.join(BASE_DIR, "metadata.pkl")


def build_index(directory: str) -> list[str]: 

    print("Starting Index Build")

    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )

    print(f"Scanning and processing directory: {directory}")

    all_chunks = []

    metadata = []

    processed_files = set()
    for filepath, text_content in process_directory(directory):
        if not text_content.strip():
            continue

        processed_files.add(os.path.basename(filepath))

        print (f"Chunking: {os.path.basename(filepath)}")

        chunks = text_splitter.split_text(text_content)
        all_chunks.extend(chunks)

        for chunk in chunks:
            metadata.append({'source': filepath, 'content': chunk})
    

    if not all_chunks:
        print("No text was found. Aborting index build")
        return []
    
    print(f"Total documents processed: {len(all_chunks)}")

    print("\n Creating embeddings for all text chunks")
    embeddings = model.encode(all_chunks, show_progress_bar=True)

    embeddings = np.array(embeddings, dtype='float32')

    print(f"Embeddings created successfully.")

    print("Building FAISS Index...")

    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)

    index.add(embeddings)

    print(f"Index built, total vectors: {index.ntotal}")

    print(f"Saving index to {INDEX_PATH} and metada to {METADATA_PATH}")

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)


    print("Index build complete")
    return sorted(list(processed_files))



if __name__ == "__main__":
        import argparse

        parser = argparse.ArgumentParser(description="Build a FAISS index from documents in a directory.")
        parser.add_argument("directory", help="The path to the directory containing documents to index.")
        args = parser.parse_args()
            
        if not os.path.isdir(args.directory):
                print(f"Error: The specified path '{args.directory}' is not a valid directory.")
        else:
                build_index(args.directory)

