from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, 
        BaseUserManager, PermissionsMixin )
from django.utils import timezone

class ListUserManager(BaseUserManager):

    def create_user(self, email):
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)

class ListUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == 'wyhuang1980@gmail.com'

    @property
    def is_active(self):
        return True

class User(models.Model):
    email = models.EmailField(primary_key=True)
    last_login = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'

    def is_authenticated(self):
        return True
