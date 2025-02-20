from .views import create_userprofile
from .views import load_profile
from django.urls import path, include

urlpatterns = [
    path('api/createprofile/', create_userprofile, name='create_userprofile'),
    path('api/loadprofile/', load_profile, name='load_profile'),
]