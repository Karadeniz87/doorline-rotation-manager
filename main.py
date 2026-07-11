from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "app": "Doorline Rotation Manager",
        "status": "running"
    }
