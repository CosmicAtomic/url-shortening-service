from fastapi import FastAPI
from database import Base, engine
from routes import router

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(router)

@app.get("/")
def test():
    return {"message": "Hello World"}