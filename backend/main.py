from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="A.I.M - Asset Intelligence Matrix")

app.include_router(router)

@app.get("/")
def home():
    return {"status": "A.I.M online", "mode": "institutional AI engine"}