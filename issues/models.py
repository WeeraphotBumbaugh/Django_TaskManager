from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Issue(models.Model):
    summary = models.CharField(max_length=256)
    body = models.TextField()
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    reporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reporter"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.summary[:100]

    def get_absolute_url(self):
        pass
