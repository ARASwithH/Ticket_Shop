from django.contrib.auth.models import BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self, phone_number, id_card, password):
        if not phone_number:
            raise ValueError('Phone number must be set')

        if not id_card:
            raise ValueError('Id card must be set')

        user = self.model(
            phone_number=phone_number,
            id_card=id_card,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, id_card, password):
        user = self.create_user(
            phone_number=phone_number,
            id_card=id_card,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


# class OTPManager(BaseUserManager):
#     def create(self, phone_number):
#         user = self.model(phone_number=phone_number)
#         user.code = random.randint(1000, 9999)
#         user.save(using=self._db)
#         return user

