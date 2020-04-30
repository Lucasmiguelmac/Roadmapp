from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User needs an email address')
        if not username:
            raise ValueError('User needs a username')
        
        #Qué pasa si el user que se ingresa tiene email y username
        user = self.model(
            email=self.normalize_email(email), #Pone todo el email en minúscula
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    #Éscribir éstos métodos es un requisito según la documentación
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    # profession = models.CharField(max_length=200, blank=True, null=True)
    # location = models.CharField(max_length=300, blank=True, null=True)
    # birthdate = models.DateField() #Ver si puedo usar fecha o Django
    # bio = models.CharField(max_length=450, blank=True, null=True)

    def __str__(self):
        return self.user.username + '\'s profile'
    