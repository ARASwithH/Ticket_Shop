from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, id_card, first_name, last_name, age, password):
        if not phone_number:
            raise ValueError('Phone number must be set')

        if not id_card:
            raise ValueError('Id card must be set')

        if not first_name:
            raise ValueError('First name must be set')

        if not last_name:
            raise ValueError('Last name must be set')

        if not age:
            raise ValueError('Age must be set')

        user = self.model(
            phone_number=phone_number,
            id_card=id_card,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, id_card, first_name, last_name, age, password):
        user = self.create_user(
            phone_number=phone_number,
            id_card=id_card,
            first_name=first_name,
            last_name=last_name,
            age=age,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user
