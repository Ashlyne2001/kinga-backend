
from pprint import pprint
from django.urls import reverse
from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from accounts.utils.user_type import CUSTOMER_USER, DRIVER_USER

from core.test_utils.custom_testcase import APITestCase
from core.test_utils.create_user import create_new_user
from accounts.models import User, get_user_model
from mysettings.models import MySetting
from profiles.models import Customer, Driver, Profile
from vehicles.models import Vehicle


class TokenViewForTopUserTestCase(APITestCase):

    def setUp(self):
        
        # Create a top user1
        self.user1 = create_new_user('john')

        self.profile = Profile.objects.get(user__email='john@gmail.com')

    def test_if_TokenView_is_working_for_ADMIN_USER(self):

        data = {
            'username': 'john@gmail.com',
            'password': 'secretpass',
        }

        response = self.client.post(reverse('api:token'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.user.is_active, True)

        token = Token.objects.get(user__email=data['username'])

        result = {
            'email': self.profile.user.email,
            'name': self.profile.user.get_full_name(),
            'token': token.key,
            'user_type': self.user1.user_type,
            'reg_no': self.user1.reg_no
        }

        self.assertEqual(response.data, result)

    def test_if_TokenView_wont_work_when_user_is_not_active(self):

        u = User.objects.get(email='john@gmail.com')
        u.is_active = False
        u.save()

        data = {
            'username': 'john@gmail.com',
            'password': 'secretpass',
        }

        response = self.client.post(reverse('api:token'), data, format='json')
        self.assertEqual(response.status_code, 400)

        result = {'non_field_errors': [
            'Unable to log in with provided credentials.']}
        self.assertEqual(response.data, result)

    def test_TokenView_with_empty_email(self):

        data = {
            'username': '',
            'password': 'secretpass',
        }

        response = self.client.post(reverse('api:token'), data, format='json')

        self.assertEqual(response.status_code, 400)

        result = {'username': ['This field may not be blank.']}
        self.assertEqual(response.data, result)

    def test_TokenView_with_wrong_email(self):

        data = {
            'username': 'wrong@gmail.com',
            'password': 'secretpass',
        }

        response = self.client.post(reverse('api:token'), data, format='json')
        self.assertEqual(response.status_code, 400)

        result = {'non_field_errors': [
            'Unable to log in with provided credentials.']}
        self.assertEqual(response.data, result)

    def test_TokenView_with_wrong_password(self):

        data = {
            'username': 'john@gmail.com',
            'password': 'yunggodfdfd',
        }

        response = self.client.post(reverse('api:token'), data, format='json')

        self.assertEqual(response.status_code, 400)

        result = {'non_field_errors': [
            'Unable to log in with provided credentials.']}
        self.assertEqual(response.data, result)

    def test_TokenView_with_empty_password(self):

        data = {
            'username': 'john@gmail.com',
            'password': '',
        }

        response = self.client.post(reverse('api:token'), data, format='json')

        self.assertEqual(response.status_code, 400)

        result = {'password': ['This field may not be blank.']}
        self.assertEqual(response.data, result)

    def test_if_TokenView_is_working_for_spotcheck(self):

        data = {
            'username': 'john@gmail.com',
            'password': 'secretpass',
        }

        response = self.client.post(reverse('api:token'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.profile.user.is_active, True)

        token = Token.objects.get(user__email=data['username'])

        result = {
            'email': self.profile.user.email,
            'name': self.profile.user.get_full_name(),
            'token': token.key,
            'user_type': self.user1.user_type,
            'reg_no': self.user1.reg_no
        }

        self.assertEqual(response.data, result)


class LogoutViewForTopUserTestCase(APITestCase):
    # Test if TokenView urls  #
    def setUp(self):

        # Create a top user1
        self.user1 = create_new_user('john')

        # My client #
        # Include an appropriate `Authorization:` header on all requests.
        token1 = Token.objects.get(user__email='john@gmail.com')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)

        # Check if django user is logged in
        self.assertEqual(self.user1.is_authenticated, True)

    def test_if_logout_is_working(self):

        # Include an appropriate `Authorization:` header on all requests.
        token1 = Token.objects.get(user__email='john@gmail.com')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token1.key)

        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 200)

        token2 = Token.objects.get(user__email='john@gmail.com')

        # Make sure the user's token was not regenerated
        self.assertEqual(token1 == token2, True)

    def test_if_LogoutView_is_not_working_for_unloggedin_user(self):

        # Unlogged in user
        self.client = APIClient()

        response = self.client.get(reverse('api:logout'))
        self.assertEqual(response.status_code, 401)

class SignupView(APITestCase):

    def get_premade_payload(self):
        """
        Simplifies creating payload
        """

        payload = {
            "first_name": "Ben",
            "last_name": "Linus",
            "email": "linus@gmail.com",
            "phone": "254723223322",
            "gender": 0,
            'user_type': DRIVER_USER,
            'current_location_name': 'Nairobi',
            "password": "secretpass",
            
        }

        return payload

    def test_if_view_can_create_a_new_driver(self):

        payload = self.get_premade_payload()

        # Add vehicle fields
        payload['vehicle_model_name'] = 'Toyota'
        payload['vehicle_color'] = 'Black'
        payload['vehicle_registration_number'] = 'KCA 123X'
        payload['vehicle_year_of_manufacture'] = 2019

        response = self.client.post(reverse('api:signup'), payload, format='json')
        self.assertEqual(response.status_code, 201)

        user = get_user_model().objects.get(email=payload['email'])
        token = Token.objects.get(user=user)

        # Confirm driver profile was created
        driver = Driver.objects.get(user__email=user)

        result = {
            'email': driver.user.email,
            'name': driver.user.get_full_name(),
            'token': token.key,
            'user_type': user.user_type,
            'reg_no': driver.user.reg_no
        }

        self.assertEqual(response.data, result)

        user = get_user_model().objects.get(email=payload['email'])
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(str(user), payload['email'])
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.first_name, payload['first_name'])
        self.assertEqual(user.last_name, payload['last_name'])
        self.assertEqual(str(user.phone), payload['phone'])
        self.assertEqual(user.user_type, DRIVER_USER)
        self.assertEqual(user.is_for_testing, False)
        self.assertEqual(user.gender, 0)
        self.assertEqual((user.join_date).strftime("%B, %d, %Y"), today)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)

        # Test driver fields were created correctly
        self.assertEqual(user.driver.phone, str(254723223322))
        self.assertEqual(user.driver.current_location_name, '')
        self.assertEqual(user.driver.current_location_coordinates, {})
        self.assertEqual((user.driver.join_date).strftime("%B, %d, %Y"), today)

        # Test vehicle fields were created correctly
        vehicle = Vehicle.objects.get()

        self.assertEqual(vehicle.driver.user.email, payload['email'])
        self.assertEqual(vehicle.model_name, 'Toyota')
        self.assertEqual(vehicle.color, 'Black')
        self.assertEqual(vehicle.registration_number, 'KCA 123X')
        self.assertEqual(vehicle.year_of_manufacture, 2019)

    def test_if_view_can_create_a_new_customer(self):

        payload = self.get_premade_payload()
        payload['user_type'] = CUSTOMER_USER

        response = self.client.post(reverse('api:signup'), payload, format='json')
        self.assertEqual(response.status_code, 201)

        user = get_user_model().objects.get(email=payload['email'])
        token = Token.objects.get(user=user)

        # Confirm customer profile was created
        customer = Customer.objects.get(user__email=user)

        result = {
            'email': customer.user.email,
            'name': customer.user.get_full_name(),
            'token': token.key,
            'user_type': user.user_type,
            'reg_no': user.reg_no
        }

        self.assertEqual(response.data, result)

        user = get_user_model().objects.get(email=payload['email'])
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(str(user), payload['email'])
        self.assertEqual(user.email, payload['email'])
        self.assertEqual(user.first_name, payload['first_name'])
        self.assertEqual(user.last_name, payload['last_name'])
        self.assertEqual(str(user.phone), payload['phone'])
        self.assertEqual(user.user_type, CUSTOMER_USER)
        self.assertEqual(user.is_for_testing, False)
        self.assertEqual(user.gender, 0)
        self.assertEqual((user.join_date).strftime("%B, %d, %Y"), today)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)

        # Test customer fields were created correctly
        self.assertEqual(user.customer.phone, str(254723223322))
        self.assertEqual(user.customer.current_location_name, '')
        self.assertEqual(user.customer.current_location_coordinates, {})
        self.assertEqual((user.customer.join_date).strftime("%B, %d, %Y"), today)



        
