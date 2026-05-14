from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas import URLCreate, URLResponse, URLStatsResponse

router = APIRouter()


@router.post("/shorten", response_model=URLResponse, status_code=201)
def create_short_url(payload: URLCreate, db: Session = Depends(get_db)):
    return crud.create_url(db, payload)


@router.get("/shorten/{short_code}", response_model=URLResponse)
def get_url(short_code: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return crud.increment_access_count(db, url)


@router.put("/shorten/{short_code}", response_model=URLResponse)
def update_url(short_code: str, payload: URLCreate, db: Session = Depends(get_db)):
    url = crud.get_url_by_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return crud.update_url(db, url, payload)


@router.delete("/shorten/{short_code}", status_code=204)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    crud.delete_url(db, url)
    return Response(status_code=204)


@router.get("/shorten/{short_code}/stats", response_model=URLStatsResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    url = crud.get_url_by_code(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url