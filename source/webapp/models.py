from django.db import models

# Create your models here.
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Project(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name="Описание")
    add_at = models.DateField(verbose_name="Дата начала")
    end_at = models.DateField(verbose_name="Дата окончания", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('view_project', kwargs={"pk": self.pk})

    class Meta:
        db_table = "Projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class Task(BaseModel):
    summary = models.CharField(max_length=50, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name="Описание")
    status = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name="status", verbose_name="Статус")
    type = models.ManyToManyField("webapp.Type", related_name="types", blank=True, verbose_name="Тип")
    project = models.ForeignKey("webapp.Project", on_delete=models.CASCADE, default=1, related_name="project",
                                verbose_name="Проект")

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.status}"

    class Meta:
        db_table = "Tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Status(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Наименования")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "status"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Наименования")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Type"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
