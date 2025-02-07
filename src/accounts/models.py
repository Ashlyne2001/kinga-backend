from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.models import Group
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth.models import Permission

from core.time_utils.time_localizers import utc_to_local_datetime_with_format
from core.token_generator import RandomStringTokenGenerator

from .utils.user_type import (
    ADMIN_USER,
    USER_TYPE_CHOICES, 
    USER_GENDER_CHOICES
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(
        self, 
        email, 
        first_name, 
        last_name, 
        phone, 
        user_type, 
        password=None, 
        **extra_fields):
        """
        Creates and saves a User with the given email, first name,
        last name and password.
        """
        if not email:
            raise ValueError("Users must have an email!")
        if not first_name:
            raise ValueError("Users must have a first name!")
        if not last_name:
            raise ValueError("Users must have a last name!")
        if not phone:
            raise ValueError("Users must have a phone phone!")
        
        
        user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                user_type=user_type,
                **extra_fields,
                )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, first_name, last_name, phone, password, **extra_fields):
        user = self.create_user(
                email, 
                first_name,
                last_name,
                phone,
                ADMIN_USER,
                password,
                **extra_fields
                )
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user 

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
            verbose_name='email',
            max_length=30,
            unique=True,
            )
    first_name = models.CharField(
            verbose_name='first name',
            max_length=15
            )
    last_name = models.CharField(
            verbose_name='last name',
            max_length=15
            )
    phone = models.BigIntegerField(
            verbose_name='phone',
            # validators=[validate_phone_for_models,],
            # unique=True,
            default=0
            )# phone should only be editable through the profile model
    join_date = models.DateTimeField(
            verbose_name='join date',
            auto_now_add=True
            )
    is_active = models.BooleanField(
        verbose_name='is active',
        default=True
        )
    is_staff = models.BooleanField(
            verbose_name='is staff',
            default=False
            )
    user_type = models.IntegerField(
        verbose_name='user type',
        choices=USER_TYPE_CHOICES,
        default=ADMIN_USER
    )
    
    is_for_testing = models.BooleanField(
        verbose_name='is for testing',
        default=False
    )
    gender = models.IntegerField(
        verbose_name='gender',
        choices=USER_GENDER_CHOICES,
        )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        unique=True,
        default=0,
        db_index=True,
        editable=False
        )
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]
    
    def __str__(self):
        return "{}".format(self.email)

    def get_short_name(self):
        return self.first_name
    
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def get_join_date(self, local_timezone):
        """ Return the creation date in local time format """
        return utc_to_local_datetime_with_format(self.join_date, local_timezone)

    def get_user_timezone(self):
        """ Returns the timezone for the user """
        return settings.LOCATION_TIMEZONE
        
    def get_profile_image_url(self):
        """
        Return image url or an empty string
        """
    
        return ""

    def get_profile_reg_no(self):
        """
        Return reg_no or an empty string
        """
        return self.reg_no

    def get_assigned_user_permissions(self):

        return list(Permission.objects.filter(
            group__user=self).values_list('codename', flat=True))

    # TODO #36 Test group has perm
    def group_has_atleast_1_perm(self, passed_perms):

        user_perms = self.get_assigned_user_permissions()
        
        perms_count = 0
        for perm in passed_perms:
            if perm in user_perms: 
                perms_count += 1
            
        return perms_count > 0

    def group_has_perm(self, perm):
        return perm in self.get_assigned_user_permissions()

    def create_profile_if_missing(self):

        from profiles.models import Profile

        if not Profile.objects.filter(user=self).exists():
            Profile.objects.get_or_create(
                user=self,
                phone=self.phone,
                reg_no=self.reg_no
            ) # Create Profile

    def save(self, *args, **kwargs):
        
        """ If reg_no is 0 get a unique reg_no """
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel
            
            """ Get the model class """ 
            model = (self.__class__)
            
            self.reg_no = GetUniqueRegNoForModel(model)
            
        super(User, self).save(*args, **kwargs) # Call the "real" save() method.

class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name_plural = "Group Proxy"


    def get_all_perms(self):

        return list(self.permissions.all().values_list('codename', flat=True))

#---------------- Start user group model --------------------------
class UserGroup(Group):
    ident_name = models.CharField(
        verbose_name='ident name',
        max_length=50
    )
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        unique=True,
        default=0,
        db_index=True,
        editable=False,
    )

    def __str__(self):
        return str(self.ident_name)

    def get_employee_count(self):
        return User.objects.filter(groups=self).count()

    def get_user_permissions_state(self):
        """
        Returns a dict with permissions codename as key and a boolean value 
        indicating if the group has the permission or not
        """

        from accounts.create_permissions import PERMISSION_DEFS

        perms = [
            p[0] for p in self.permissions.all().order_by('id').values_list('codename')
        ]

        state = {}
        for key, _value in PERMISSION_DEFS.items():
            state[key] = key in perms
            
        return state

    def save(self, *args, **kwargs):
        
        """ If reg_no is 0 get a unique reg_no """
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel
            
            """ Get the model class """
            model = (self.__class__)
            
            self.reg_no = GetUniqueRegNoForModel(model)
            
        super(UserGroup, self).save(*args, **kwargs) 


#---------------- Start user session model --------------------------   
class UserSession(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}".format(self.user.email)

#---------------- End user session model -------------------------- 
    
#---------------- Start user channel record model --------------------------
class UserChannelRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_api = models.BooleanField(
            verbose_name='is api',
            default=False) 
    channel_name = models.CharField(
            verbose_name='channel name',
            max_length=100,
            )
        
    def __str__(self):
        return str(self.channel_name)

#---------------- End user channel record model --------------------------

#---------------- Start websocket ticket model --------------------------
class WebSocketTicket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reg_no = models.BigIntegerField(
        verbose_name='reg no',
        unique=True,
        default=0,
        db_index=True,
        editable=False
        )

    def __str__(self):
        return "{}".format(self.user.email)

    def save(self, *args, **kwargs):
        
        """ If reg_no is 0 get a unique reg_no """
        if not self.reg_no:
            from core.reg_no_generator import GetUniqueRegNoForModel
                
            """ Get the model class """
            model = (self.__class__)
            
            self.reg_no = GetUniqueRegNoForModel(model)
                
        super(WebSocketTicket, self).save(*args, **kwargs) # Call the "real" save() method.
    
#---------------- End websocket ticket model --------------------------


#---------------- Start reset password token utils --------------------------
class ResetPasswordToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # Key field, though it is not the primary key of the model
    key = models.CharField(
        verbose_name='key',
        max_length=64,
        db_index=True,
        unique=True
    )
    created_date = models.DateTimeField(
        verbose_name='created date',
        default=timezone.now,)

    def generate_key(self):
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return RandomStringTokenGenerator().generate_token()

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ResetPasswordToken, self).save(*args, **kwargs)


def clear_expired(expiry_time):
    """
    Remove all expired tokens
    :param expiry_time: Token expiration time
    """
    ResetPasswordToken.objects.filter(created_date__lte=expiry_time).delete()

#---------------- End reset password token utils --------------------------
