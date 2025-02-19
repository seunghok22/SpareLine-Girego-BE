from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from json.decoder import JSONDecodeError
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import os
from allauth.socialaccount.models import SocialAccount
from .serializers import UserProfileSerializer


User = get_user_model()
load_dotenv()
EMAIL_HOST = os.getenv('EMAIL_HOST')

# 로그인 페이지 연결
def google_login(request):
   scope = os.getenv('GOOGLE_SCOPE_USERINFO')        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{os.getenv('GOOGLE_REDIRECT')}?client_id={os.getenv('GOOGLE_CLIENT_ID')}&response_type=code&redirect_uri={os.getenv('GOOGLE_REDIRECT')}&scope={scope}")

# 인가 코드를 받아 로그인 처리
def google_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={os.getenv('GOOGLE_CLIENT_ID')}&client_secret={os.getenv('GOOGLE_CLIENT_SECRET')}&code={code}&grant_type=authorization_code&redirect_uri={os.getenv('GOOGLE_REDIRECT')}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    google_access_token = token_req_json.get('access_token')

    email_response = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_access_token}")
    res_status = email_response.status_code

    if res_status != 200:
        return JsonResponse({"status": 400,"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    
    email_res_json = email_response.json()
    email = email_res_json.get('email')
	
    try:
        user = User.objects.get(email=email)
        if user is None: #계정이 없으면 추가하기기
            return JsonResponse({"status": 404,"message": "User Account Not Exists"}, status=status.HTTP_404_NOT_FOUND) 
        
        # 소셜로그인 계정 유무 확인
        social_user = SocialAccount.objects.get(user=user)  
        if social_user.provider != "google":
            return JsonResponse({"status": 400,"message": "User Account Not Exists"}, status=status.HTTP_400_BAD_REQUEST) 
            
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
		
        res = JsonResponse(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return res
    except:
        serializer = UserProfileSerializer(data=request.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)