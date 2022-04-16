from django.urls import path
from . import views

app_name = 'followers'
urlpatterns = [
    path('follow/', views.user_follow, name="user_follow"),
]
