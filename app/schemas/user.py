from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True) 