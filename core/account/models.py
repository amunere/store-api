from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '+78889999000'. Up to 11 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)    
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    objects = UserManager()
    
    def __str__(self):
        return "{}".format(self.email)