from django.db import models
from django.contrib.auth.models import User

class Charity(models.Model):
    name = models.CharField(max_length=31)
    slug = models.SlugField()
    description = models.TextField()
    founded_date = models.DateField()
    contact = models.EmailField()
    website = models.URLField()

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'
        verbose_name_plural = "charities"

    def __str__(self):
        return self.name


class Donor(models.Model):
    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=61)
    last_login = models.DateField()

    class Meta:
        ordering = ['first_name', 'last_name']
        get_latest_by = 'last_login'

    def __str__(self):
        return self.first_name + " " + self.last_name


class Donation(models.Model):
    donor = models.ForeignKey(User)
    charity = models.ForeignKey(Charity)
    amount = models.IntegerField()

    def __str__(self):
        return self.donor + " " + self.charity + " " + self.amount
