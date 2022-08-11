from django.urls import path


from webapp.views.project import ListProject, CreateProject, ProjectView
from webapp.views.tasks import IndexView, CreateTask, TaskView, UpdateTask, DeteleTask

urlpatterns = [
    path('task/list/', IndexView.as_view(), name="index"),
    path('task/<int:pk>/add/', CreateTask.as_view(), name="add"),
    path('task/<int:pk>/', TaskView.as_view(), name="view"),
    path('task/<int:pk>/update', UpdateTask.as_view(), name="update"),
    path('task/<int:pk>/delete', DeteleTask.as_view(), name="delete"),
    path('', ListProject.as_view(), name="index_list"),
    path('project/add/', CreateProject.as_view(), name="add_project"),
    path('project/<int:pk>/', ProjectView.as_view(), name="view_project")
]
