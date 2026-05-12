from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import string
import random
from datetime import datetime

app = FastAPI()

urls = []

class URLCreate(BaseModel):
    url: HttpUrl


count =0

@app.get('/')
def test():
    return JSONResponse(content={"message": "Hello World"})

@app.post('/shorten')
def create_short_url(URLRequest : URLCreate):
    existing_url = next((item for item in urls if item.get("url") == str(URLRequest.url)), None)
    if existing_url:
        return JSONResponse(status_code=400, content={"error": "URL has already been shortened"})

    letters = string.ascii_letters
    digits = string.digits
    existing_codes = {item["shortCode"] for item in urls}
    while True:
        short_url = ''.join(random.choices(letters, k=4) + random.choices(digits, k=3))
        if short_url not in existing_codes:
            break
    time_created = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    url_content = {
            "id": len(urls) +1,

            "url": str(URLRequest.url),
            "shortCode": short_url,
            "createdAt": time_created,
            "updatedAt": time_created,
            "accessCount": 0
        }
    urls.append(url_content)
    return JSONResponse(
        status_code=201,
        content= url_content
    )

@app.get('/shorten/{short_code}')
def get_url(short_code: str):
    existing_url = next((item for item in urls if item.get("shortCode") == short_code), None)
    if not existing_url:
        return JSONResponse(status_code=404, content={"error": "URL not found"})
    existing_url["accessCount"] += 1
    
    return JSONResponse(status_code=200, content= existing_url) 

@app.put('/shorten/{short_code}')
def update_url(URLRequest : URLCreate, short_code: str):
    url = next((item for item in urls if item.get("shortCode") == short_code), None)
    if not url:
        return JSONResponse(status_code=404, content={"error": "URL not found"})
    url["url"] = str(URLRequest.url)
    url["updatedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return JSONResponse(status_code=200, content=url)

@app.delete('/shorten/{short_code}')
def delete_url(short_code: str):
    url = next((item for item in urls if item.get("shortCode") == short_code), None)
    if not url:
        return JSONResponse(status_code=404, content={"error": "URL not found"})
    urls.remove(url)
    return JSONResponse(status_code=204, content= None)

@app.get('/shorten/{short_code}/stats')
def get_stats(short_code: str):
    url = next((item for item in urls if item.get("shortCode") == short_code), None)
    if not url:
        return JSONResponse(status_code=404, content={"error": "URL not found"})
    return JSONResponse(
        status_code=200,
        content={
            "id": url["id"],
            "url": url["url"],
            "shortCode": url["shortCode"],
            "createdAt": url["createdAt"],
            "updatedAt": url["updatedAt"],
            "accessCount": url["accessCount"]
        }
    )
    