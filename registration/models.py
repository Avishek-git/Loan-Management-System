from django.db import models

# Create your models here.

class User(models.Model):
    uuid = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.uuid

