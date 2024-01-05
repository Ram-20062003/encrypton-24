
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from sqlmodel import Session, select
from server.controller.auth import get_current_user, get_password_hash, verify_password
from server.models.schema import *
from config.database import get_database
from server.models.user import UserBase, UserLogin
from server.controller.auth import sign_jwt, JWTBearer



router = APIRouter(
    prefix="/auth",
)

@router.post("/login")
async def login(
    login_user: UserLogin,
    database: Session = Depends(get_database)
):
    user = database.exec(select(User).where(User.email == login_user.email)).first()

    if not user:
         raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(login_user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    if not user.id:
        raise HTTPException(status_code=401, detail="Invalid User")
    
    
    jwt_token = sign_jwt(user.email, user.name, user.id)
    
    try:
        del user.password
        del user.id
        del user.mobile_no
    except KeyError:
        pass

    return {"token": jwt_token, "user": user}

@router.post("/register")
async def register(
    user: UserBase,
    database: Session = Depends(get_database)
):
    existing_user = database.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
         raise HTTPException(status_code=401, detail="Email already registered")

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        name=user.name,
        mobile_no=user.mobile_no,
    )

    database.add(new_user)
    database.commit()
    database.close()

    return {"message": "User created successfully"}


@router.post("/test-auth")
async def sample_test_auth(
    bearer_token: str = Depends(JWTBearer()),
    database: Session = Depends(get_database)
):
    user = get_current_user(bearer_token, database)
    return {"message": "You are authorized", "user": user}

    
    





