from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']
        widgets = {
            'type': widgets.CheckboxSelectMultiple
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) > 20:
            raise ValidationError("Описания должно быть короче 20 символов")
        return description


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'add_at', 'end_at']

