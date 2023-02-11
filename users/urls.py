from django.urls import path
from .views import RegisterUserView, LoginUserView, LogoutUserView, UpdateProfileView

urlpatterns = [
    path('api/v1/signup/', RegisterUserView.as_view(), name='user_register'),

    path('api/v1/login/', LoginUserView.as_view(), name='user_login'),
    path('api/v1/logout/', LogoutUserView.as_view(), name='user_logout'),
    path('api/v1/update_profile/<str:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
]
