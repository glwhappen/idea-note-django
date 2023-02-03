from django.db import models


# Create your models here.
class Note(models.Model):
    id = models.CharField(primary_key=True, max_length=40, unique=True, null=False, blank=False)
    content = models.CharField(max_length=5000)
    contentMd5 = models.CharField(max_length=40, default='')  # 内容的md5值，在更新时判断上一次的更新是否等于这个md5值，防止内容覆盖
    background = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    state = models.IntegerField()
    secret = models.BooleanField()
    type = models.CharField(max_length=40, default='')
    author = models.CharField(max_length=40, default='')
    public = models.BooleanField(default=False) # 文章是否公开
    top = models.IntegerField(default=0) # 文章置顶 0 默认 小于零置底 大于零置顶
    createAt = models.DateTimeField()
    updateAt = models.DateTimeField()

