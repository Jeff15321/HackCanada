from fastapi import FastAPI
from routes.jobs import router
import uvicorn

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
app = FastAPI(
    title="O*NET API",
    description="API for querying O*NET job titles and tasks",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def index():
    return {"message": "app is working"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )