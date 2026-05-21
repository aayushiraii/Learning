from langchain_community.document_loaders import (
    UnstructuredPowerPointLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from main import store_embedding

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


pptx_docs = load_pptx_files("data")

# Chunking Configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50
)

for doc in pptx_docs:

    text = doc.page_content

    metadata = doc.metadata

    chunks = text_splitter.split_text(text)

    print(f"\nTotal Chunks Created: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):

        print(f"\nStoring Chunk {index}")

        print(f"Chunk Length: {len(chunk)}")

        store_embedding(chunk, metadata)


print("\nAll PPTX Embeddings Stored")