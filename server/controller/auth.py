from passlib.context import CryptContext
import jwt as JWT
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from sqlmodel import Session

from config.settings import settings
from server.models.schema import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


jwt_secret = settings.jwt_secret
jwt_algo = "HS256"


def jwt_response(token: str):
    return {"jwt_token": token}


def get_current_user(token: str, database: Session):
    payload = decode_jwt(token)
    user_id: int = payload.get("user_id",-1)
    user = database.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def sign_jwt(user_email: str, user_name: str,user_id: int) -> dict[str, str]:
    payload = {
        "user_email": user_email,
        "user_name": user_name,
        "user_id": user_id,
    }
    token = JWT.encode(payload=payload, key=jwt_secret, algorithm=jwt_algo)

    return jwt_response(token)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = JWT.decode(
            token, jwt_secret, algorithms=[jwt_algo]
        )
        return decoded_token
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Access: JWT Invalid",
        ) from exception


def verify_jwt(jwtoken: str) -> bool:
    """
    Verify the JWT Token
    """
    is_token_valid: bool = False

    try:
        payload = decode_jwt(jwtoken)
    except Exception as exception:
        payload = None
        raise HTTPException(
            status_code=403,
            detail="Invalid token or expired token.",
        ) from exception

    if payload:
        is_token_valid = True
    return is_token_valid



class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):

        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        credentials = await super().__call__(
            request)
        if not credentials:
            raise HTTPException(
                status_code=403, detail="Invalid request."
            )
        try:
            if not credentials.scheme == "Bearer":

                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme.",
                )
            if not verify_jwt(credentials.credentials):
                
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token.",
                )
            return credentials.credentials
        except Exception as exception:
            
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            ) from exception

