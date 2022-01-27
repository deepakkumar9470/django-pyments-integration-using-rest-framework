from django.db import models
from django.core import validators
# Create your models here.



class Producst(models.Model):
    email = models.EmailField(max_length=254, default='test@gmail.com')
    paid = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    description = models.CharField(default=None,max_length=800)
    def __str__(self):
        return self.email








