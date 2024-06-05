from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    velocity = models.IntegerField(null=False)

    def __str__(self):
        return self.name