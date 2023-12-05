from django.db import models
from model_utils import Choices
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.postgres.fields import ArrayField



# from ckeditor.fields import RichTextField


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    



class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Account(models.Model):
    """Employees"""
    SUPER = 1
    ADMIN = 2
    STANDARD = 3

    USER_TYPE = [
        (SUPER, 'Super Admin'),
        (ADMIN, 'Admin'),
        (STANDARD, 'Standard'),
    ]

    GENDER = Choices(
       (1, 'male'),
       (2, 'female')
    )

    MARTIAL_STATUS = Choices(
        (1, 'Single'),
        (2, 'Married')
    )

    ACTIVE = 1
    INCOMPLETE_PROFILE = 2
    FOR_ACTIVATION = 3
    SUSPENDED = 4
    DELETED = 5

    STATUS = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
        (DELETED, 'Deleted'),
        (INCOMPLETE_PROFILE, 'Incomplete Profile'),
        (FOR_ACTIVATION, 'For Activation'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_user',
        db_index=True,
        blank=True,
        null=True
    )

    client = models.ForeignKey(
        "Client",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to="profile",
        null=True,
        blank=True,
        default=None
    )
    gender = models.IntegerField(choices=GENDER)
    date_hired = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.IntegerField(choices=USER_TYPE, default=STANDARD)

    status = models.IntegerField(choices=STATUS, default=ACTIVE)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Client(models.Model):
    ACTIVE = 1
    INCOMPLETE_PROFILE = 2
    FOR_ACTIVATION = 3
    SUSPENDED = 4
    DELETED = 5

    STATUS = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
        (DELETED, 'Deleted'),
        (INCOMPLETE_PROFILE, 'Incomplete Profile'),
        (FOR_ACTIVATION, 'For Activation'),
    ]

    company_name = models.CharField(max_length=255, null=False, blank=False)
    company_url = models.URLField(max_length=200, null=True, blank=True)
    logo = models.ImageField(
        upload_to="client_logo",
        null=True,
        blank=True,
        default=None
    )
    address_1 = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name='client_created_by',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(choices=STATUS, default=ACTIVE)

    def __str__(self):
        return self.company_name
    
class Category(models.Model):
    FIXED_CATEGORY = (
        ('raw materials', 'Raw Materials'),
        ('office supplies', 'Office Supplies'),
        ('hardware', 'Hardware'),
    )
    name = models.CharField(max_length=255, choices=FIXED_CATEGORY)
    new_category = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class RawItem(models.Model):
    name= models.CharField(max_length=255)
    qty = models.FloatField(max_length=100)
    def __str__(self):
        return self.name

class IngredientMeasurement(models.Model):
    PIECES = 1
    BOX = 2
    TABLESPOON = 3
    MEASURE_CHOICES  = [
        (PIECES, 'PCS'),
        (BOX, 'BX'),
        (TABLESPOON, 'TBLSPN'),
    ]
    value = models.FloatField(max_digits=100, decimal_places=2)
    unit = models.IntegerField(MEASURE_CHOICES, on_delete=models.CASCADE)
    item= models.ForeignKey(RawItem(on_delete=models.CASCADE), blank=True, null=True)
    def __str__(self):
     return f" {self.item} {self.value} {self.unit}"
    

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS = Choices('draft', 'published', 'archived')
    name = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20)
    recipes = models.ManyToManyField(IngredientMeasurement(on_delete=models.CASCADE), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    tags = models.ManyToManyField(Tag, related_name='items')

    def __str__(self):
        return self.name
    

   