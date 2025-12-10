from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

# Create your models here.

# This UserManager will have two Methods and does not contain any fields.
# One method for creating Regular User and another method is for creating super user
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')
    
    # start creating an user 
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password) # set_password method is for storing password in encoding format
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

# The User class will have typical fields name like first_name, Last_name etc.
# By inheriting this AbstractBaseUser methond enaable us to take full control of ediing the whole custer user model
# including authenticational functionlity of django.
# There is another method call AbstarctUser which will only addtion fields in the model, not any control. 
# by AbstractBaseUser method we can set for example email addess is the login option
class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique= True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # Required Fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # Authentication field set
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Set the username that will use 
    # Set this model as user authentication model in settings.py

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    # This function is use to get and check the user role. 
    # Accordingly user will redirect to the set dashboard

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

class UserProfile(models.Model):
    # ForeignKey is used when One use can have multiple profile
    # OneToOneField is used when one user can have one profile only
    # CASCADE- If user is deleted then simultaneously profile also get deleted
    # Media folder need to created for picture purpose.
    # For image pillow package is reuired to install
    # Django signal will use to create the profile automatically when the user will create
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) 
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    addess_line_1 = models.CharField(max_length=50, blank=True, null=True)
    addess_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modifed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email