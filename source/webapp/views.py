from audioop import reverse

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from webapp.forms import TaskForm, SearchForm
from webapp.models import Task



class IndexView(ListView):
    model = Task
    template_name = "index.html"
    context_object_name = "tasks"
    ordering = ("-updated_at",)
    paginate_by = 2


    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        if self.search_value:
            return Task.objects.filter(Q(summary__contains=self.search_value) | Q(description__contains=self.search_value))
        return Task.objects.all()


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context ['query'] = query
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")



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