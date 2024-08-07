import datetime

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from core.test_utils.create_user import create_new_user

from core.test_utils.custom_testcase import APITestCase
from profiles.models import Customer, Driver
from trips.models import Trip

class TripIndexViewTestCase(APITestCase):

    def setUp(self):

        # Create customer user and profile
        self.customer_user = create_new_user('john')
        self.customer_profile = Customer.objects.create(
            user=self.customer_user,
            current_location_name='Nairobi',
            current_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
        )

        # Create driver user and profile
        self.driver_user = create_new_user('jack')
        self.driver_profile = Driver.objects.create(
            user=self.driver_user,
            current_location_name='Nairobi',
            current_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
        )

        # Create 3 Trips
        self.trip1 = Trip.objects.create(
            driver=self.driver_profile,
            customer=self.customer_profile,
            from_location_name='Nairobi',
            destination_location_name='Mombasa',
            from_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
            destination_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
            start_time=timezone.now(),
            end_time=timezone.now() + datetime.timedelta(hours=8),
            is_completed=True,
        )

        self.trip2 = Trip.objects.create(
            driver=self.driver_profile,
            customer=self.customer_profile,
            from_location_name='Nairobi',
            destination_location_name='Nakuru',
            from_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
            destination_location_coordinates={
                'lat': 1.0,
                'lng': 3.0,
            },
            start_time=timezone.now(),
            end_time=timezone.now() + datetime.timedelta(hours=2),
            is_completed=True,
        )

        self.trip3 = Trip.objects.create(
            driver=self.driver_profile,
            customer=self.customer_profile,
            from_location_name='Nairobi',
            destination_location_name='Nyeri',
            from_location_coordinates={
                'lat': 1.0,
                'lng': 2.0,
            },
            destination_location_coordinates={
                'lat': 1.0,
                'lng': 4.0,
            },
            start_time=timezone.now(),
            end_time=timezone.now() + datetime.timedelta(hours=1),
            is_completed=True,
        )

        # Include an appropriate `Authorization:` header on all requests.
        token = Token.objects.get(user__email='john@gmail.com')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_view_is_returning_a_user_profile(self):
        
        response = self.client.get(reverse('api:trip_index'))
        self.assertEqual(response.status_code, 200)

        results = {
            'count': 3, 
            'next': None, 
            'previous': None, 
            'results': [
                {
                    'cost': 'Ksh 0.00',
                    'driver_name': self.trip3.get_driver_name(), 
                    'customer_name': self.trip3.get_customer_name(),
                    'from_location_name': self.trip3.from_location_name,
                    'destination_location_name': self.trip3.destination_location_name,
                    'from_location_coordinates': self.trip3.from_location_coordinates,
                    'destination_location_coordinates': self.trip3.destination_location_coordinates,
                    'start_time': self.trip3.get_start_time(),
                    'end_time': self.trip3.get_end_time(),
                    'is_completed': self.trip3.is_completed,
                    'reg_no': self.trip3.reg_no,
                }, 
                {
                    'cost': 'Ksh 0.00',
                    'driver_name': self.trip2.get_driver_name(), 
                    'customer_name': self.trip2.get_customer_name(),
                    'from_location_name': self.trip2.from_location_name,
                    'destination_location_name': self.trip2.destination_location_name,
                    'from_location_coordinates': self.trip2.from_location_coordinates,
                    'destination_location_coordinates': self.trip2.destination_location_coordinates,
                    'start_time': self.trip2.get_start_time(),
                    'end_time': self.trip2.get_end_time(),
                    'is_completed': self.trip2.is_completed,
                    'reg_no': self.trip2.reg_no,
                }, 
                {
                    'cost': 'Ksh 0.00',
                    'driver_name': self.trip1.get_driver_name(), 
                    'customer_name': self.trip1.get_customer_name(),
                    'from_location_name': self.trip1.from_location_name,
                    'destination_location_name': self.trip1.destination_location_name,
                    'from_location_coordinates': self.trip1.from_location_coordinates,
                    'destination_location_coordinates': self.trip1.destination_location_coordinates,
                    'start_time': self.trip1.get_start_time(),
                    'end_time': self.trip1.get_end_time(),
                    'is_completed': self.trip1.is_completed,
                    'reg_no': self.trip1.reg_no,
                }
            ]
        }

        self.assertEqual(response.data['results'][0], results['results'][0])
