from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import requests
from env import USER_API

class GeneralAuthorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(GeneralAuthorization, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(GeneralAuthorization, self).__call__(request)

        # Check user
        req = requests.post(
            f"{USER_API}/user/authorization",
            headers = {
                "Authorization": f"Bearer {credentials.credentials}"
            }
        )

        if req.status_code == 200:
            return {
                "token": credentials.credentials,
                "user_id": req.json()["user_id"],
                "is_admin": req.json()["authorization"],
            }
        
        raise HTTPException(status_code=401, detail="Not authenticate.")