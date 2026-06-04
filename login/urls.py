from django.urls import path
from login.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
]