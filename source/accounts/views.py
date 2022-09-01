from django.contrib.auth import  get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator


from django.contrib.auth import login

from django.shortcuts import  redirect

from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm
from accounts.models import Profile


User = get_user_model()

class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('index_profile')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    paginate_by = 2
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.get_object().projects.all(), self.paginate_by, self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_object
        context['projects'] = page_object.object_list
        context['is_paginated'] = page_object.has_other_pages()
        return context


class ListProfile(PermissionRequiredMixin, ListView):
    model = User
    template_name = "index_profile.html"
    context_object_name = "users"


    def has_permission(self):
        return 'Project Manager' in self.request.user.groups.all().values_list('name', flat=True) or \
               'Team Lead' in self.request.user.groups.all().values_list('name', flat=True)



class ChangeProfileView(LoginRequiredMixin, UpdateView):
    model=User
    form_class = UserChangeForm
    template_name = 'change_profile.html'
    profile_form_class = ProfileChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context ['profile_form'] = self.profile_form_class(instance=self.get_object().profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        profile_form = self.profile_form_class(instance=self.object.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)


    def get_object(self, queryset=None):
        return self.request.user



    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return redirect('profile', self.object.pk)

    def form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))


class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})