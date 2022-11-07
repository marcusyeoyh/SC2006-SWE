from django.urls import path
from .views import UserDetailAPI, RegisterUserAPIView, LoginView, FavouriteView

urlpatterns = [
    path('get-details/', UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('login/', LoginView.as_view()),
    path('favourites/', FavouriteView.as_view()),
]