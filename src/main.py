from fastapi import FastAPI

app = FastAPI(title="FastAPI Backend Template")

@app.get("/health")
def health_check():
    return {"status": "ok"}

