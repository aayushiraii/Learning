from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader
)

from main import process_documents

import os


def load_docx_files(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".docx"):

            file_path = os.path.join(folder_path, file)

            loader = UnstructuredWordDocumentLoader(file_path)

            docs = loader.load()

            documents.extend(docs)

            print(f"\nDOCX Loaded: {file}")

    return documents


docx_docs = load_docx_files(os.getenv("DATA_FILE"))

process_documents(docx_docs)

print("\nAll DOCX Embeddings Stored")