# URL Shortening Service

A REST API for shortening URLs, built with FastAPI and PostgreSQL.

Project page: https://roadmap.sh/projects/url-shortening-service

## Requirements

- Python 3.10+
- PostgreSQL

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CosmicAtomic/url-shortening-service.git
   cd url-shortening-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic[email]
   ```

4. Create a `.env` file in the project root:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/yourdbname
   ```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/shorten` | Create a short URL |
| `GET` | `/shorten/{short_code}` | Retrieve original URL |
| `PUT` | `/shorten/{short_code}` | Update original URL |
| `DELETE` | `/shorten/{short_code}` | Delete a short URL |
| `GET` | `/shorten/{short_code}/stats` | Get URL stats including access count |

## Interactive Docs

Once running, visit `http://localhost:8000/docs` for the auto-generated Swagger UI.
