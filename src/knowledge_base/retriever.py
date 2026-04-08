def retrieve_chunks(query, chunks, top_k=3):
    results = []
    query = query.lower()

    for chunk in chunks:
        text = chunk["text"].lower()
        score = 0

        for word in query.split():
            if word in text:
                score += 1

        if score > 0:
            results.append((score, chunk))

    results.sort(key=lambda x: x[0], reverse=True)

    return [item[1] for item in results[:top_k]]






