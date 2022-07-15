from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import TaskForm
from webapp.models import Task



class IndexView(View):
    def get(self, request, *args, **kwargs):
        task = Task.objects.order_by("-updated_at")
        context = {"tasks": task}
        return render(request, "index.html", context)


class ArticleView(TemplateView):
    template_name = "article_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        kwargs["tasks"] = task
        return super().get_context_data(**kwargs)


class Create(View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get("summary")
            status = form.cleaned_data.get("status")
            type = form.cleaned_data.get("type")
            description = form.cleaned_data.get("description")
            new_task = Task.objects.create(summary=summary, status=status, type=type, description=description)
            return redirect("view", pk=new_task.pk)
        return render("create.html", {"form": form})

