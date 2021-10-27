from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=False)
    name = models.CharField(max_length=200, blank=True, null=False)
    image = models.FileField(upload_to='', null=False)
    text = models.TextField(null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class BookSlug(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=56)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug