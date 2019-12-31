from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):

    """ CUSTOM USER MODEL """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOISES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))

    avatar = models.ImageField(upload_to="avatars", blank=True,)
    gender = models.CharField(choices=GENDER_CHOISES, max_length=10, blank=True,)
    bio = models.TextField(default="", blank=True,)
    birthday = models.DateField(blank=True, null=True,)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False,)
