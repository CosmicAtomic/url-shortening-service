from pydantic import BaseModel, HttpUrl, ConfigDict

class URLCreate(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    shortCode: str
    createdAt: str
    updatedAt: str

class URLStatsResponse(URLResponse):
    accessCount: int