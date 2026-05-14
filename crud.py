import secrets
import string
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import URL
from schemas import URLCreate



def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _generate_unique_short_code(db: Session, length: int = 7) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if not db.query(URL).filter(URL.shortCode == code).first():
            return code


def get_url_by_code(db: Session, short_code: str) -> URL | None:
    return db.query(URL).filter(URL.shortCode == short_code).first()

def create_url(db: Session, payload: URLCreate) -> URL:
    now = _now_iso()
    new_url = URL(
        url=str(payload.url),
        shortCode=_generate_unique_short_code(db),
        createdAt=now,
        updatedAt=now,
        accessCount=0,
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def update_url(db: Session, url: URL, payload: URLCreate) -> URL:
    url.url = str(payload.url)
    url.updatedAt = _now_iso()
    db.commit()
    db.refresh(url)
    return url

def delete_url(db: Session, url: URL) -> None:
    db.delete(url)
    db.commit()

def increment_access_count(db: Session, url: URL) -> URL:
    url.accessCount += 1
    db.commit()
    db.refresh(url)
    return url