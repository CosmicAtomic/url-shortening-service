from fastapi import FastAPI, HTTPException, Response 
from pydantic import BaseModel, HttpUrl
import string
import secrets  
from datetime import datetime, timezone 

app = FastAPI()

urls = []
next_id = 1 

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

def _find(short_code: str):
    return next((item for item in urls if item["shortCode"] == short_code), None)

@app.get('/')
def test():
    return {"message": "Hello World"}

@app.post("/shorten", response_model=URLResponse, status_code=201)
def create_short_url(payload: URLCreate): 
    global next_id
    alphabet = string.ascii_letters + string.digits
    existing_codes = {item["shortCode"] for item in urls}
    while True:
        short_code = "".join(secrets.choice(alphabet) for _ in range(7))
        if short_code not in existing_codes:
            break

    now = _now_iso()
    url_content = {
        "id": next_id,
        "url": str(payload.url),
        "shortCode": short_code,
        "createdAt": now,
        "updatedAt": now,
        "accessCount": 0,
    }
    next_id += 1
    urls.append(url_content)

    return url_content

@app.get("/shorten/{short_code}", response_model=URLResponse)
def get_url(short_code: str):
    url = _find(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url["accessCount"] += 1
    return url

@app.put("/shorten/{short_code}", response_model=URLResponse) 
def update_url(short_code: str, payload: URLCreate): 
    url = _find(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")  # CHANGED
    url["url"] = str(payload.url)
    url["updatedAt"] = _now_iso()
    return url

@app.delete("/shorten/{short_code}", status_code=204)  
def delete_url(short_code: str):
    url = _find(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    urls.remove(url)
    return Response(status_code=204)

@app.get("/shorten/{short_code}/stats", response_model=URLStatsResponse)
def get_stats(short_code: str):
    url = _find(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url