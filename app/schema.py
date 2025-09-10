from pydantic import BaseModel


class ReverseIPCreate(BaseModel):
    original_ip: str
    reversed_ip: str


class ReverseIPResponse(BaseModel):
    id: int
    original_ip: str
    reversed_ip: str
    created_at: str

    class Config:
        from_attributes = True
