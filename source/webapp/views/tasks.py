from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from webapp.forms import TaskForm, SearchForm
from webapp.models import Task, Project


class IndexView(ListView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    ordering = ("-created_at",)
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Task.objects.filter(
                Q(status__name__icontains=self.search_value) | Q(summary__icontains=self.search_value))
        return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context["query"] = query
            context["search"] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class TaskView(DetailView):
    template_name = "tasks/task_view.html"
    model = Task


class CreateTask(CreateView):
    form_class = TaskForm
    template_name = "tasks/create.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_project', kwargs={'pk': self.object.project.pk})


class UpdateTask(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        tasks = get_object_or_404(Task, pk=pk)
        form = TaskForm(initial={
            "summary": tasks.summary,
            "status": tasks.status,
            "description": tasks.description,
            "type": tasks.type.all()
        })
        return render(request, "tasks/update.html", {'form': form})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        tasks = get_object_or_404(Task, pk=pk)
        form = TaskForm(data=request.POST)
        if form.is_valid():
            tasks.delete()
            tasks = form.save()
            return redirect("view", pk=tasks.pk)
        return render(request, "tasks/update.html", {'form': form})


class DeteleTask(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        return render(request, "tasks/delete.html", {"tasks": task})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect("index")
