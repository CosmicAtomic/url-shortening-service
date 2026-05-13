from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel, HttpUrl
import string
import secrets  
from datetime import datetime, timezone 
from database import Base, engine , get_db
from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import Session

app = FastAPI()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key= True, autoincrement= True)
    url= Column(String)
    shortCode = Column(String, unique= True)
    createdAt= Column(String)
    updatedAt= Column(String)
    accessCount = Column(Integer)

Base.metadata.create_all(engine)

class URLCreate(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    id: int
    url: str
    shortCode: str
    createdAt: str
    updatedAt: str

class URLStatsResponse(URLResponse):
    accessCount: int

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _find(short_code: str, db: Session = Depends(get_db)):
    return db.query(URL).filter(URL.shortCode == short_code).first()

@app.get('/')
def test():
    return {"message": "Hello World"}

@app.post("/shorten", response_model=URLResponse, status_code=201)
def create_short_url(payload: URLCreate,db: Session = Depends(get_db)): 
    alphabet = string.ascii_letters + string.digits
    existing_codes = {url.shortCode for url in db.query(URL).all()}
    while True:
        short_code = "".join(secrets.choice(alphabet) for _ in range(7))
        if short_code not in existing_codes:
            break

    now = _now_iso()
    new_url = URL(
        url = str(payload.url),
        shortCode =short_code,
        createdAt= now,
        updatedAt = now,
        accessCount = 0,
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url

@app.get("/shorten/{short_code}", response_model=URLResponse)
def get_url(short_code: str, db: Session = Depends(get_db)):
    url = _find(short_code, db)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url.accessCount += 1
    db.commit()
    db.refresh(url)
    return url

@app.put("/shorten/{short_code}", response_model=URLResponse) 
def update_url(short_code: str, payload: URLCreate, db: Session = Depends(get_db)): 
    url = _find(short_code, db)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found") 
    url.url = str(payload.url)
    url.updatedAt = _now_iso()
    db.commit()
    db.refresh(url)
    return url

@app.delete("/shorten/{short_code}", status_code=204 )  
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url = _find(short_code, db)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return Response(status_code=204)

@app.get("/shorten/{short_code}/stats", response_model=URLStatsResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url = _find(short_code, db)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url