from pydantic import BaseModel

class User(BaseModel):
    npm: int
    username: str
    name: str

class Authenticate(BaseModel):
    ticket: str
    service: str

class AdminAuth(BaseModel):
    username: str
    password: str

class Dockerfile(BaseModel):
    text: str

class NPM(BaseModel):
    npm: int