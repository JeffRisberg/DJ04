from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from . import query


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = query.BaseQuerySet.as_manager()

    class Meta:
        abstract = True


class TaggedItem(models.Model):
    tag_name = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    tagged_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag_name


class Charity(models.Model):
    name = models.CharField(max_length=31)
    slug = models.SlugField()
    description = models.TextField()
    founded_date = models.DateField()
    contact = models.EmailField()
    website = models.URLField()
    tags = GenericRelation(TaggedItem)

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
    tags = GenericRelation(TaggedItem)

    class Meta:
        ordering = ['first_name', 'last_name']
        get_latest_by = 'last_login'

    def __str__(self):
        return self.first_name + " " + self.last_name


class Donation(BaseModel):
    donor = models.ForeignKey(User)
    charity = models.ForeignKey(Charity)
    amount = models.IntegerField()
    tags = GenericRelation(TaggedItem)

    def __str__(self):
        return self.donor + " " + self.charity + " " + self.amount
