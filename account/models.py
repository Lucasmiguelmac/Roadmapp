from django.conf import Settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core import validators
from django.core.files.storage import default_storage as storage
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField
from PIL import Image
from roadmaps.models import Tag




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


#Clases para usar en profile
class SocialNetwork(models.Model):
    whatsapp_number = models.IntegerField(db_index=True, unique=False, blank=True, null=True)
    telegram_username = models.CharField(validators=[validators.MinLengthValidator(5)], max_length=32, db_index=True, unique=False, blank=True, null=True)
    personal_site = models.URLField(max_length=128, db_index=True, unique=False, blank=True, null=True)
    linkedin_profile = models.CharField(validators=[validators.MinLengthValidator(5)], max_length=128, db_index=True, unique=False, blank=True, null=True)
    github_profile = models.URLField(max_length=128, db_index=True, unique=False, blank=True, null=True)
    twitter_username = models.CharField(validators=[validators.MinLengthValidator(5)], max_length=32, db_index=True, unique=False, blank=True, null=True)
    instagram_username = models.CharField(validators=[validators.MinLengthValidator(5)], max_length=32, db_index=True, unique=False, blank=True, null=True)
    blog = models.URLField(max_length=128, db_index=True, unique=False, blank=True, null=True)
    youtube_channel = models.URLField(max_length=128, db_index=True, unique=False, blank=True, null=True)
    stackoverflow_profile = models.URLField(max_length=128, db_index=True, unique=False, blank=True, null=True)
    reddit_username = models.CharField(validators=[validators.MinLengthValidator(5)], max_length=32, db_index=True, unique=False, blank=True, null=True)
    facebook_profile = models.URLField(max_length=128, db_index=True, unique=False, blank=True, null=True)
    show_email = models.BooleanField(default=False, db_index=True, unique=False)
    
    
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(default='images/logo.png', upload_to='profile_pics')
    bio = models.CharField(max_length=450, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    social_networks = models.OneToOneField(SocialNetwork, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    interests = models.ManyToManyField(Tag, blank=True)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    show_activity = models.BooleanField(default=True)
    following = models.ManyToManyField('self', blank=True, related_name='followers', through='Follow')

    #Editamos el método .save() de éste model para atajar la imágen antes y achicarla a un cuadrado
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.profile_pic:
            size = 200, 200
            image = Image.open(self.profile_pic)
            image.thumbnail(size, Image.ANTIALIAS)
            fh = storage.open(self.profile_pic.name, "w")
            format = 'png'
            image.save(fh, format)
            fh.close()

    def __str__(self):
        return str(self.user.username) + '\'s profile'
    
class Follow(models.Model): #Ésta tabla: https://stackoverflow.com/questions/40069192/django-models-database-design-for-user-and-follower
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following_targets')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

# Creamos la tabla que se va a encargar del historial de la persona
class History(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True) #Roadmaps, Units y en el futuro Questions o Posts
    object_id = models.PositiveIntegerField() #Primary key del objeto en su tabla
    content_object = GenericForeignKey() #El objeto
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_type)

    class Meta:
        verbose_name_plural = 'Histories'




