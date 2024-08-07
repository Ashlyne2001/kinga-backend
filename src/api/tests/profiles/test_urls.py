from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from core.test_utils.create_user import create_new_user

from core.test_utils.custom_testcase import APITestCase
from profiles.models import Customer, Driver


class CustomerProfileViewTestCase(APITestCase):

    def setUp(self):

        # Create top user
        self.user1 = create_new_user('john')

        # Create customer profile
        self.customer_profile1 = Customer.objects.create(
            user=self.user1,
            current_location_name='Nairobi',
            current_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
        )
        
        # Include an appropriate `Authorization:` header on all requests.
        token = Token.objects.get(user__email='john@gmail.com')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_view_is_returning_a_user_profile(self):
        
        response = self.client.get(reverse('api:customer_profile'))
        self.assertEqual(response.status_code, 200)

        results = {
            'full_name': 'John Lock', 
            'email': 'john@gmail.com', 
            'phone': '', 
            'current_location_name': 'Nairobi', 
            'current_location_coordinates': {
                'lat': 1.0, 
                'lng': 2.0
            }, 
            'join_date': self.customer_profile1.get_join_date(), 
            'last_login_date': False
        }

        self.assertEqual(response.data, results)


class DriverProfileViewTestCase(APITestCase):

    def setUp(self):

        # Create top user
        self.user1 = create_new_user('john')

        # Create driver profile
        self.driver_profile1 = Driver.objects.create(
            user=self.user1,
            current_location_name='Nairobi',
            current_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
        )
        
        # Include an appropriate `Authorization:` header on all requests.
        token = Token.objects.get(user__email='john@gmail.com')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_view_is_returning_a_user_profile(self):
        
        response = self.client.get(reverse('api:driver_profile'))
        self.assertEqual(response.status_code, 200)

        results = {
            'full_name': 'John Lock', 
            'email': 'john@gmail.com', 
            'phone': '', 
            'current_location_name': 'Nairobi', 
            'current_location_coordinates': {
                'lat': 1.0, 
                'lng': 2.0
            }, 
            'join_date': self.driver_profile1.get_join_date(), 
            'last_login_date': False
        }

        self.assertEqual(response.data, results)
    
    