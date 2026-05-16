from fastapi import FastAPI

app = FastAPI(title="Student Roster API")


@app.get("/health")
def health():
    return {"status": "ok"}
