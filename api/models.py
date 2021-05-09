from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True,max_length=225)
    full_name = models.CharField(max_length=225)
    date_joined=models.DateField(auto_now_add=True)
    is_staff=models.BooleanField(default=False)
    contacts=models.ManyToManyField('Contact')

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    class META:
        verbose_name='user'
        verbose_name_plural='users'


class Contact(models.Model):
    country_code=models.CharField(max_length=225)
    full_name=models.CharField(max_length=225)
    phone_number=models.CharField(max_length=10)
    is_favorite=models.BooleanField(default=False)
    custom_id=models.PositiveIntegerField()

