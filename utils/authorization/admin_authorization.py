from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import requests
from env import USER_API

class AdminAuthorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AdminAuthorization, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AdminAuthorization, self).__call__(request)

        req = requests.post(
            f"{USER_API}/user/authorization",
            headers = {
                "Authorization": f"Bearer {credentials.credentials}"
            }
        )

        if (req.status_code) == 200 and (req.json()["authorization"]):
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Not admin.")