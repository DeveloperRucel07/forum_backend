from django.urls import path
from .views import LoginView, RegistrationView, LogoutView
urlpatterns = [
    path('login/',LoginView.as_view(), name = 'login'),
    path('registration/',RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name = 'logout')
]