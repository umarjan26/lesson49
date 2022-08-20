from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registration/', RegisterView.as_view(), name="registration")
]