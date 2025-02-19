# urls.py
from django.urls import path, include
from .views import google_login
from .views import google_callback

urlpatterns = [
    # 구글 소셜로그인
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    # path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]