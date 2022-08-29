from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, ProfileView, ListProfile

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registration/', RegisterView.as_view(), name="registration"),
    path('<int:pk>/', ProfileView.as_view(), name="profile"),
    path('list/', ListProfile.as_view(), name="list_profile")
]