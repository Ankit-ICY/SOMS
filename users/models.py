# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, name=None, password=None):
        if not email and not phone:
            raise ValueError("Either email or phone must be provided")

        user = self.model(email=self.normalize_email(email) if email else None,
                          phone=phone,
                          name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, name, password):
        user = self.create_user(email=email, phone=phone, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.role = CustomUser.Roles.SUPERADMIN
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Super Admin'
        ADMIN = 'admin', 'Admin'
        NORMAL = 'normal', 'Normal'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.ADMIN)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email if self.email else self.phone

    @property
    def is_superadmin(self):
        return self.role == self.Roles.SUPERADMIN

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_normal(self):
        return self.role == self.Roles.NORMAL

