from langchain_community.document_loaders import (
    UnstructuredPowerPointLoader
)

from main import process_documents

import os


def load_pptx_files(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".pptx"):

            file_path = os.path.join(folder_path, file)

            loader = UnstructuredPowerPointLoader(file_path)

            docs = loader.load()

            documents.extend(docs)

            print(f"\nPPTX Loaded: {file}")

    return documents


pptx_docs = load_pptx_files(os.getenv("DATA_FILE"))

process_documents(pptx_docs)

print("\nAll PPTX Embeddings Stored")