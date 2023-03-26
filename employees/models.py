from django.db import models
from django.core.validators import MaxValueValidator


class Employee(models.Model):
    """
    Employee Model
    """

    GENDERS = (
        ("M", "M"),
        ("F", "F"),
        ("T", "T"),
    )
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(60)])
    gender = models.CharField(max_length=1, choices=GENDERS)
    department = models.CharField(max_length=100)
    salary = models.PositiveIntegerField()

    def __str__(self):
        return self.name
