from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.schemas.request.auth import LoginRequestModel
from app.schemas.response.auth import LoginResponseModel
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponseModel,
)
def login(
    request: LoginRequestModel,
    # db: Session = Depends(get_db),
):
    service = AuthService()

    return service.login(request)