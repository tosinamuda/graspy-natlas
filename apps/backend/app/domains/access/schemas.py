from pydantic import BaseModel

class VerifyAccessRequest(BaseModel):
    code: str

class VerifyAccessResponse(BaseModel):
    valid: bool
