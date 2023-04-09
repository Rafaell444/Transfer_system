from django.contrib.auth import get_user
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class File(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    transfer_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    host = models.EmailField()

    def __str__(self):
        return f"{self.transfer_to.email} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.id:
            request = kwargs.pop('request', None)
            if request and request.user.is_authenticated:
                self.host = request.user.email  # set the host field to the email of the authenticated user
        super().save(*args, **kwargs)
