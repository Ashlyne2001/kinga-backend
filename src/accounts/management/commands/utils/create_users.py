from django.contrib.auth import get_user_model
from accounts.utils.user_type import DRIVER_USER

from profiles.models import Profile
from core.test_utils.create_user import create_new_user

User = get_user_model()

def _create_testing_user():
    
    email = 'testing@gmail.com'

    user_exists = get_user_model().objects.filter(email=email).exists()

    if not user_exists:

        User.objects.create_user(
            email=email,
            first_name='Just For',
            last_name='Testing',
            phone='254720113322',
            user_type=DRIVER_USER,
            is_for_testing=True,
            gender=0,
            password='kingapass',
        )

        
        
def create_app_initial_users():
    _create_testing_user()
  
