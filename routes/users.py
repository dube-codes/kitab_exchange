from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from database import get_session
from models.user import User, UserCreate, UserUpdate, UserRead

from auth import verify_api_key

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    existing = session.exec(select(User).where(User.email == user_data.email)).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.!"
        )

    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[UserRead])
def user_list(session: Session = Depends(get_session)):
    list = session.exec(select(User)).all()
    return list
