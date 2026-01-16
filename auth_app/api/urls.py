from django.urls import path
from .views import LoginView, RegistrationView, CookieTokenObtainPairView, CookieTokenRefreshView
urlpatterns = [

    path('registration/',RegistrationView.as_view(), name='registration'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]