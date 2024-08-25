from fastapi import FastAPI
from mangum import Mangum
from src.controller.slack_controller import router as slack_router

app = FastAPI()

app.include_router(slack_router, prefix="/slack")

@app.get("/")
def read_root():
    return {"message": "Lambda with FastAPI is running."}

handler = Mangum(app)
