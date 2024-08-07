import random

from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.utils.user_type import ADMIN_USER

from core.time_utils.time_localizers import utc_to_local_datetime

from profiles.models import Profile

User = get_user_model()


# =========================== Top User =======================================

def initial_data_for_top_user_profile(user):

    # Save initial data for profile
    profile = Profile.objects.get(user=user)
    profile.business_name = 'Skypac'
    profile.location = 'Nairobi'
    profile.save()


def create_top_user_assets(
        first_name,
        last_name,
        phone,
        gender,
        created_date=utc_to_local_datetime(timezone.now())):

    user = User.objects.create_user(
        email='{}@gmail.com'.format(first_name.lower()),
        first_name=first_name.title(),
        last_name=last_name,
        phone=phone,
        user_type=ADMIN_USER,
        gender=gender,
        password='secretpass',
    )

    initial_data_for_top_user_profile(user)

    return user


def create_new_user(user, created_date=utc_to_local_datetime(timezone.now())):

    if user == 'super':
        super_user = User.objects.create_superuser(
            email='john@gmail.com',
            first_name='John',
            last_name='Lock',
            phone='254710223322',
            gender=0
        )
        super_user.set_password('secretpass')

        initial_data_for_top_user_profile(super_user)

        return super_user

    elif user == 'john':

        created_user = create_top_user_assets(
            'John',
            'Lock',
            '254710223322',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'jack':

        created_user = create_top_user_assets(
            'Jack',
            'Shephard',
            '254720223322',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'testing':
        created_user = create_top_user_assets(
            'Testing',
            'User',
            '254713223344',
            gender=1,
            created_date=created_date)

        return created_user

    elif user == 'cristina':

        created_user = create_top_user_assets(
            'Cristina',
            'Yang',
            '254713223355',
            gender=1,
            created_date=created_date)

        return created_user

    elif user == 'izzie':

        created_user = create_top_user_assets(
            'Izzie',
            'Stevens',
            '254713223366',
            gender=1,
            created_date=created_date)

        return created_user

    elif user == 'george':

        created_user = create_top_user_assets(
            'George',
            'Omalley',
            '254713223377',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'miranda':

        created_user = create_top_user_assets(
            'Miranda',
            'Bailey',
            '254713223388',
            gender=1,
            created_date=created_date)

        return created_user

    elif user == 'derek':

        created_user = create_top_user_assets(
            'Derek',
            'Shephard',
            '254713223399',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'callie':

        created_user = create_top_user_assets(
            'Callie',
            'Torres',
            '254713223312',
            gender=1,
            created_date=created_date)

        return created_user

    elif user == 'mark':

        created_user = create_top_user_assets(
            'Mark',
            'Sloan',
            '254713223313',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'owen':

        created_user = create_top_user_assets(
            'Owen',
            'Hunt',
            '254713223314',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'arizona':

        created_user = create_top_user_assets(
            'Arizona',
            'Robbins',
            '254713223315',
            gender=1,
            created_date=created_date)

        return created_user

    elif user == 'walt':

        created_user = create_top_user_assets(
            'Walt',
            'Lloyd',
            '254713223316',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'micheal':

        created_user = create_top_user_assets(
            'Micheal',
            'Dawson',
            '254713223317',
            gender=0,
            created_date=created_date)

        return created_user

    elif user == 'teddy':

        created_user = create_top_user_assets(
            'Tedy',
            'Altman',
            '254713223318',
            gender=1,
            created_date=created_date)

        return created_user

def get_random_safcom_number():
    # Produces unique phones

    phone = '25470{}{}{}{}{}{}{} '.format(
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9),
        random.randint(0, 9))

    return phone
