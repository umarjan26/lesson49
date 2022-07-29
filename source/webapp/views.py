from audioop import reverse

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from webapp.forms import TaskForm
from webapp.models import Task



class IndexView(ListView):
    model = Task
    template_name = "index.html"
    context_object_name = "tasks"
    ordering = ("-updated_at",)
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        print(context)
        return context



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
            type = form.cleaned_data.pop("type")
            description = form.cleaned_data.get("description")
            new_task = Task.objects.create(summary=summary, status=status, description=description)
            new_task.type.set(type)
            return redirect("view", pk=new_task.pk)
        return render("create.html", {"form": form})



class Update(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        tasks = get_object_or_404(Task, pk=pk)
        form = TaskForm(initial={
            "summary": tasks.summary,
            "status": tasks.status,
            "description": tasks.description,
            "type": tasks.type.all()
        })
        return render(request, "update.html", {'form': form})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        tasks = get_object_or_404(Task, pk=pk)
        form = TaskForm(data=request.POST)
        if form.is_valid():
            tasks.summary = form.cleaned_data.get("summary")
            tasks.status = form.cleaned_data.get("status")
            tasks.type.set(form.cleaned_data.pop("type"))
            tasks.description = form.cleaned_data.get("description")
            tasks.save()
            return redirect("view", pk=tasks.pk)
        return render(request, "update.html", {'form': form})



class Delete(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        return render(request, "delete.html", {"tasks": task})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect("index")