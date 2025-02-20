from .views import create_userprofile
from django.urls import path, include

urlpatterns = [
    path('api/createprofile/', create_userprofile, name='create_userprofile'),
]