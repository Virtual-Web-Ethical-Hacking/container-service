from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
AUTH_API = config["AUTH_API"]

class UserAuthorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(UserAuthorization, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(UserAuthorization, self).__call__(request)

        req = requests.post(
            f"{AUTH_API}/user/authorization",
            headers = {
                "Authorization": f"Bearer {credentials.credentials}"
            }
        )

        if req.status_code == 200:
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Not user.")