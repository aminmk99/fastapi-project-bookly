from typing import Optional
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi import Request, status

from .utils import decode_token


class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )
            
        if token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token=token)

        return True if token_data is not None else False
