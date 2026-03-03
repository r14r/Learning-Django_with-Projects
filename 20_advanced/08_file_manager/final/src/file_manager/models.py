import os
from django.db import models
from django.contrib.auth.models import User


def user_upload_path(instance, filename):
    return f'uploads/{instance.owner.pk}/{filename}'


class Folder(models.Model):
    name       = models.CharField(max_length=255)
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    parent     = models.ForeignKey('self', on_delete=models.CASCADE,
                                   null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'parent', 'name')

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    owner         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    folder        = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='files')
    original_name = models.CharField(max_length=255)
    file          = models.FileField(upload_to=user_upload_path)
    mime_type     = models.CharField(max_length=100, blank=True)
    size          = models.BigIntegerField(default=0)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

    @property
    def extension(self):
        return os.path.splitext(self.original_name)[1].lower()

    @property
    def size_kb(self):
        return round(self.size / 1024, 1)
