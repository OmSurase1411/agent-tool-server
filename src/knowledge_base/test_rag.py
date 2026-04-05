from loader import load_documents
from chunker import chunk_text

docs = load_documents("src/knowledge_base/documents")

for doc in docs:
    print(f"\nDocument: {doc['filename']}")
    
    chunks = chunk_text(doc["content"], doc["filename"])
    
    print(f"Number of chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks[:2]):  # show first 2 chunks
        print(f"Chunk {i+1}: {chunk['text'][:100]}...")