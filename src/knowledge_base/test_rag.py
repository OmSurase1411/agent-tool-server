from loader import load_documents
from chunker import chunk_text
from retriever import retrieve_chunks

docs = load_documents("src/knowledge_base/documents")

for doc in docs:
    print(f"\nDocument: {doc['filename']}")
    
    chunks = chunk_text(doc["content"], doc["filename"])
    
    print(f"Number of chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks[:2]):  # show first 2 chunks
        print(f"Chunk {i+1}: {chunk['text'][:100]}...")
    
all_chunks = []

for doc in docs:
    chunks = chunk_text(doc["content"], doc["filename"])
    all_chunks.extend(chunks)

query = "customer data policy"

results = retrieve_chunks(query, all_chunks)

print("\nRetrieved Chunks:\n")

for res in results:
    print(f"Source: {res['source']}")
    print(res["text"][:100], "\n")

