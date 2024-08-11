from pydantic import BaseModel


class ContainerInformation(BaseModel):
    username: str
    password: str
