import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from enum import Enum
from core.utils.file_path import dataset_file_path


class Topic(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, default=uuid.uuid4)
    description = models.TextField(blank=True, null=True)
    user_created = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="topics", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"{self.id}, [{self.slug}] {self.name}"

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.slug:
                self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Dataset(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="datasets", blank=False, null=False)
    name = models.CharField(max_length=50, blank=True, null=True)
    file = models.FileField(upload_to=dataset_file_path, blank=False, null=False)
    task = models.OneToOneField('Task', on_delete=models.SET_NULL, related_name="dataset", blank=True, null=True)
    user_created = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="datasets", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"{self.id}, [{self.topic.slug}] {self.file}"


class ProcessingStatus(Enum):
    STARTED = 1
    LOADING = 2
    LOADED = 3
    PREPROCESSED = 4
    CHUNKING = 5
    CHUNKED = 6
    STORING = 7
    STORED = 8
    COMPLETED = 9


class Task(models.Model):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (STARTED, "Started"),
        (SUCCESS, "Success"),
        (ERROR, "Error"),
    ]
    task_id = models.CharField(max_length=100, unique=True, db_index=True)
    queue = models.CharField(max_length=50, blank=True, null=True)
    kwargs = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    current_state = models.CharField(max_length=50, blank=True, null=True, default="pending")
    result = models.JSONField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    log = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"{self.id}, {self.task_id}"


class History(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="histories", blank=False, null=False)
    query = models.TextField(max_length=5000, blank=True, null=True)
    answer = models.TextField(max_length=5000, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    user_created = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="histories", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # noinspection PyUnresolvedReferences
    def __str__(self):
        return f"{self.id}, [{self.topic.slug}] {self.user_created.username}"
