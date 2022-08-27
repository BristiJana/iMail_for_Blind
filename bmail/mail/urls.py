from django.urls import path
from mail.views import Home, front
from django.urls import path

app_name = "mail"

urlpatterns = [
    path('', Home, name="home"),
    
    # path("", front, name="front"),
]