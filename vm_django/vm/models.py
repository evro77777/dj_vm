from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class QueryVM(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pool = models.CharField(max_length=100)
    subdivision = models.CharField(max_length=100)
    name_vm = models.CharField(max_length=100)
    ram = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(8)
    ])
    cpu_cores = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(8)
    ])
    ssd = models.IntegerField(validators=[
        MinValueValidator(10),
        MaxValueValidator(150)
    ])
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_vm
