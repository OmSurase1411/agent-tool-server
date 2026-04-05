def chunk_text(text, filename, chunk_size=100, overlap=20):
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk,
            "source": filename
        })

        start += chunk_size - overlap
        chunk_id += 1

    return chunks