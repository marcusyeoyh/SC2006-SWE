from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone

"""
Overrides django's base user model
"""
class UserManager(BaseUserManager):
    def create_user(
        self, 
        email,
        first_name,
        last_name,
        password=None,
    ):
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        return self.create_user(email, first_name, last_name, password)





class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    # User information
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    # Admin information
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active.",
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    # Override base model
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Allows access to the user's name as a property rather than a function
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("email",)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    email = User.email
    block = models.IntegerField(blank=True, null=True)
    street_name = models.TextField(blank=True, null=True)
    predictedprice = models.IntegerField(db_column='PredictedPrice', blank=True, null=True)  # Field name made lowercase.
    flat_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favourite'
