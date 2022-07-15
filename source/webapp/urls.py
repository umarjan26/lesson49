from django.urls import path
from django.views.generic import TemplateView, RedirectView

from webapp.views import IndexView, Create, ArticleView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('add/', Create.as_view(), name="add"),
    path('task/<int:pk>/', ArticleView.as_view(), name="view")

]
