from django.db import models
from apps.user.models import *

class ProjectModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BugModel(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='assigned_bugs')
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='created_bugs')

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    bug = models.ForeignKey(BugModel, on_delete=models.CASCADE)
    commenter = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"Comment by {self.commenter.name}"
