from django import forms
from django.forms import widgets

from webapp.models import Type, Status


class TaskForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label="Summary")
    description = forms.CharField(max_length=2000, label="Description",
                                  widget=widgets.Textarea(attrs={"cols": 30, "rows": 2}))
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all())