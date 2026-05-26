from langchain_community.document_loaders import CSVLoader

from main import process_documents

import os


def load_csv_files(folder_path):

    documents = []

    for file in os.listdir(folder_path):

        if file.endswith(".csv"):

            file_path = os.path.join(folder_path, file)

            loader = CSVLoader(file_path=file_path)

            docs = loader.load()

            documents.extend(docs)

            print(f"\nCSV Loaded: {file}")

    return documents


csv_docs = load_csv_files(os.getenv("DATA_FILE"))

process_documents(csv_docs)

print("\nAll CSV Embeddings Stored")