from django.db import models
from core import models as core_models

# third party import
from django_countries.fields import CountryField

# etc import
from users import models as user_models

# Create your models here.


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()

    # country library
    # https://github.com/SmileyChris/django-countries

    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()

    check_in = models.TimeField()
    check_out = models.TimeField()

    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
