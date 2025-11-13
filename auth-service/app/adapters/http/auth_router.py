from fastapi import APIRouter, Depends, HTTPException, status, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .schemas import (
    SignupRequest, LoginRequest, TokenResponse, RefreshTokenRequest,
    AccessTokenResponse, ChangePasswordRequest, UpdateProfileRequest,
    UserProfileResponse, VerifyTokenResponse
)

router = APIRouter()
bearer = HTTPBearer(auto_error=False)

def get_auth_service(request: Request):
    return request.app.container.auth_service  # type: ignore[attr-defined]

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    auth_service = Depends(get_auth_service),
):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        user_info = await auth_service.verify_token(credentials.credentials)
        return user_info
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: SignupRequest, auth_service = Depends(get_auth_service)):

    try:
        result = await auth_service.signup(body.email, body.password, body.full_name)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, auth_service = Depends(get_auth_service)):

    try:
        result = await auth_service.login(body.email, body.password)
        return TokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(body: RefreshTokenRequest, auth_service = Depends(get_auth_service)):

    try:
        result = await auth_service.refresh_token(body.refresh_token)
        return AccessTokenResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=UserProfileResponse)
async def get_profile(user_info = Depends(get_current_user), auth_service = Depends(get_auth_service)):

    try:
        user = await auth_service.get_user_profile(user_info["user_id"])
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except KeyError:
        raise HTTPException(404, "User not found")

@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    body: UpdateProfileRequest,
    user_info = Depends(get_current_user),
    auth_service = Depends(get_auth_service)
):

    try:
        user = await auth_service.update_profile(user_info["user_id"], body.full_name)
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_login=user.last_login
        )
    except KeyError:
        raise HTTPException(404, "User not found")

@router.post("/change-password")
async def change_password(
    body: ChangePasswordRequest,
    user_info = Depends(get_current_user),
    auth_service = Depends(get_auth_service)
):

    try:
        await auth_service.change_password(user_info["user_id"], body.old_password, body.new_password)
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except KeyError:
        raise HTTPException(404, "User not found")

@router.post("/verify", response_model=VerifyTokenResponse)
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    auth_service = Depends(get_auth_service)
):

    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    try:
        user_info = await auth_service.verify_token(credentials.credentials)
        return VerifyTokenResponse(**user_info)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
