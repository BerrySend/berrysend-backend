from fastapi import status
from app.iam.application.user_application_service import UserApplicationService
from app.iam.interfaces.resources.sign_in_request import SignInRequest
from app.iam.interfaces.resources.sign_up_request import SignUpRequest
from main import app

user_app_service = UserApplicationService()

@app.post("/auth/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(request: SignUpRequest):
    try:
        await user_app_service.sign_up(request.username, request.password)
        return request
    except Exception as e:
        return {"error": str(e)}

@app.post("/auth/sign-in", status_code=status.HTTP_200_OK)
async def sign_in(request: SignInRequest):
    try:
        return await user_app_service.sign_in(request.username, request.password)
    except Exception as e:
        return {"error": str(e)}

@app.post("/auth/change-password", status_code=status.HTTP_200_OK)
async def change_password(user_id: str, old_password: str, new_password: str):
    try:
        await user_app_service.change_password(user_id, old_password, new_password)
        return {"message": "Password changed successfully"}
    except Exception as e:
        return {"error": str(e)}