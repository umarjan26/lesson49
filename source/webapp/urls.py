from django.urls import path
from django.views.generic import TemplateView, RedirectView

from webapp.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index")
]