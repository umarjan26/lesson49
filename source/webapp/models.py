from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Task(BaseModel):
    summary = models.CharField(max_length=50, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name="Описание")
    status = models.ForeignKey("webapp.Status", on_delete=models.PROTECT, related_name="status", verbose_name="Статус")
    type = models.ForeignKey("webapp.Type", on_delete=models.PROTECT, related_name="types", verbose_name="Тип")

    def __str__(self):
        return f"{self.id}. {self.summary}: {self.status}"

    class Meta:
        db_table = "Tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Status(BaseModel):
    name = models.CharField(max_length=50, default="", null=False, blank=False, verbose_name="Наименования")

    def __str__(self):
        return f"{self.id}. {self.name}"

    class Meta:
        db_table = "status"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Наименования")

    def __str__(self):
        return f"{self.id}. {self.name}"

    class Meta:
        db_table = "Type"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
