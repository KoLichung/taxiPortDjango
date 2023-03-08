from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
        user = self.model(
            email = email, 
            name=extra_fields.get('name'),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.CharField(max_length=125, unique=True, default='')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Case(models.Model):
    user =  models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank = True
    )
    user_name = models.CharField(max_length=128, default='', blank = True, null=True)
    user_email = models.CharField(max_length=20, default='', blank = True, null=True)

    CASE_TYPE_CHOICES = [
        ('direct','direct'),
        ('reserve','reserve'),
    ]
    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES, default='direct') 

     #(wait, way_to_catch, arrived, catched, on_road, finished, canceled)
    CASE_STATE_CHOICES = [
        ('wait', 'wait'),
        ('way_to_catch', 'way_to_catch'),
        ('arrived', 'arrived'),
        ('catched', 'catched'),
        ('on_road', 'on_road'),
        ('finished', 'finished'),
        ('canceled', 'canceled'),
    ]
    case_state = models.CharField(max_length=20, choices=CASE_STATE_CHOICES, default='') 

    is_english = models.BooleanField(default=False)

    on_lat = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null=True)
    on_lng = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null=True)
    on_address = models.CharField(max_length=255, default='', blank = True, null=True)
    on_address_en = models.CharField(max_length=255, default='', blank = True, null=True)

    off_lat = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null=True)
    off_lng = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null=True)
    off_address = models.CharField(max_length=255, default='', blank = True, null=True)
    off_address_en = models.CharField(max_length=255, default='', blank = True, null=True)

    driver_name = models.CharField(max_length=255, default='', blank = True, null=True)
    car_model = models.CharField(max_length=128, default='', blank = True, null=True)
    car_id_number = models.CharField(max_length=128, default='', blank = True, null=True)
    expect_minutes = models.IntegerField(default=0, blank = True, null=True)

    case_money = models.IntegerField(default=0, blank = True, null=True)

    create_time = models.DateTimeField(auto_now=False, blank = True, null=True)
    confirm_time = models.DateTimeField(auto_now=False, blank = True, null=True)
    arrived_time = models.DateTimeField(auto_now=False, blank = True, null=True)
    catched_time = models.DateTimeField(auto_now=False, blank = True, null=True)
    off_time = models.DateTimeField(auto_now=False, blank = True, null=True)

    reserve_date_time = models.DateTimeField(auto_now=False, blank = True, null=True)

    feedback = models.TextField(default='', blank = True, null=True)
