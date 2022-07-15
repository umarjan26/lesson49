from django.shortcuts import render
from django.views import View

from webapp.models import Task




class IndexView(View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.order_by("-updated_at")
        context = {"task": task}
        return render(request, "index.html", context)

