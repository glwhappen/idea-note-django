from django.db import models


# Create your models here.
class Note(models.Model):
    id = models.CharField(primary_key=True, max_length=40, unique=True, null=False, blank=False)
    content = models.CharField(max_length=5000)
    background = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    state = models.IntegerField()
    secret = models.BooleanField()
    type = models.CharField(max_length=40, default='')
    author = models.CharField(max_length=40, default='')
    createAt = models.DateTimeField()
    updateAt = models.DateTimeField()

