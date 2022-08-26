from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from webapp.forms import SearchForm, ProjectForm, UserForm
from webapp.models import Project


class ListProject(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"
    ordering = ("-created_at",)
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Project.objects.filter(
                Q(name__icontains=self.search_value))
        return Project.objects.all()

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


class CreateProject(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"


class ProjectView(DetailView):
    template_name = "projects/view.html"
    model = Project


class UpdateProject(UpdateView):
    form_class = ProjectForm
    template_name = 'projects/update.html'
    model = Project


class DeleteProject(DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('index_list')


class AddUser (UpdateView):
    model = Project
    form_class = UserForm
    template_name = 'projects/add_user.html'

