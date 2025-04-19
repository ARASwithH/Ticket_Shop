from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
import random


# Create your models here.


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    id_card = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, perm, obj=None):
        return True


class OTPcode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.code} - {self.phone_number}'

    @classmethod
    def create_otp(cls, phone_number):
        code = str(random.randint(1000, 9999))
        otp = cls.objects.create(phone_number=phone_number, code=code)
        return otp
