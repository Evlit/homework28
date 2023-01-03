from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=200, default='')
    author = models.CharField(max_length=100, default='')
    price = models.FloatField(default=0)
    description = models.TextField()
    address = models.CharField(max_length=200, default='')
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100, default='')