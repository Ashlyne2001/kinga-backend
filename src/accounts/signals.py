from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_out

from rest_framework.authtoken.models import Token
from accounts.utils.user_type import DRIVER_USER, ADMIN_USER
from profiles.models import Customer, Driver

from .models import UserSession

@receiver(post_save, sender=get_user_model())
def create_ADMIN_USER_addittional_models_signal(sender, instance, created, **kwargs):
    """
    Creates Profile, Token, MySetting and 3 UserGroup models (Owner, Manager, 
    Cashier)"""
    
    """ Profile and MySetting are imported here to prevent cyclic imports errors """
    from profiles.models import Profile

    if created:

        # Create Token
        Token.objects.create(user=instance)  

        # Create Profile
        if instance.user_type == ADMIN_USER:
            
            Profile.objects.get_or_create(
                user=instance,
                phone=instance.phone,
                reg_no=instance.reg_no
            ) 
            
        elif instance.user_type == DRIVER_USER:
            
            Driver.objects.get_or_create(   
                user=instance,
                phone=instance.phone,
                reg_no=instance.reg_no
            )

        else:
            Customer.objects.get_or_create(
                user=instance,
                phone=instance.phone,
                reg_no=instance.reg_no
            )

        
            
@receiver(post_save, sender=Session)
def session_created_signal(sender, instance, created, **kwargs):
    
    if created:
        
        session_user_id = instance.get_decoded().get('_auth_user_id')
        
        if session_user_id:
            user = get_user_model().objects.get(pk=session_user_id)
            session_id = instance.session_key
            
            UserSession.objects.get_or_create(
                    user = user,
                    session_id = session_id)


# User logout signal
def user_logged_out_handler(sender, request, user, **kwargs):
    from .utils.logout_users import logout_user_everywhere
    logout_user_everywhere(user)
    
user_logged_out.connect(user_logged_out_handler)        
   