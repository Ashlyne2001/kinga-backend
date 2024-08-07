from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from django.db.utils import IntegrityError
from accounts.management.commands.utils.create_users import create_app_initial_users
from django.contrib.auth.models import Group, Permission
from accounts.utils.user_type import CUSTOMER_USER, DRIVER_USER
from core.test_utils.create_user import create_new_user
from core.test_utils.custom_testcase import TestCase
from mysettings.models import MySetting
from profiles.models import Profile
from core.test_utils.date_utils import DateUtils
"""
=========================== User ===================================
"""
class UserTestCase(TestCase):

    def setUp(self):
        
        #Create a user with email john@gmail.com
        self.user = create_new_user('john') 

    def create_second_class_user(self, user_type=DRIVER_USER):

        user = get_user_model().objects.create_user(
            first_name='Ben',
            last_name='Linus',
            email='ben@gmail.com',
            phone='254723223322',
            user_type=user_type,
            gender=0,
            password='secretpass',
        )

        return user

    def test_creating_driver_user_(self):

        # Delete all users
        get_user_model().objects.all().delete()

        # Create a driver user
        self.create_second_class_user()

        user = get_user_model().objects.get(email='ben@gmail.com')
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(str(user), 'ben@gmail.com')
        self.assertEqual(user.email, 'ben@gmail.com')
        self.assertEqual(user.first_name, 'Ben')
        self.assertEqual(user.last_name, 'Linus')
        self.assertEqual(user.phone, 254723223322)
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

    def test_creating_customer_user_(self):

        # Delete all users
        get_user_model().objects.all().delete()

        # Create a customer user
        self.create_second_class_user(user_type=CUSTOMER_USER)

        user = get_user_model().objects.get(email='ben@gmail.com')
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(str(user), 'ben@gmail.com')
        self.assertEqual(user.email, 'ben@gmail.com')
        self.assertEqual(user.first_name, 'Ben')
        self.assertEqual(user.last_name, 'Linus')
        self.assertEqual(user.phone, 254723223322)
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



'''
    def test_create_profile_if_missing(self):

        self.assertEqual(Profile.objects.filter(user=self.user).exists(), True)

        Profile.objects.filter(user=self.user).delete()

        self.assertEqual(Profile.objects.filter(user=self.user).exists(), False)

        self.user.create_profile_if_missing()

        self.assertEqual(Profile.objects.filter(user=self.user).exists(), True)
    
    def test_verbose_names(self):
        u = get_user_model().objects.get(email='john@gmail.com')

        self.assertEqual(u._meta.get_field('email').verbose_name,'email')
        self.assertEqual(u._meta.get_field('first_name').verbose_name,'first name')
        self.assertEqual(u._meta.get_field('last_name').verbose_name,'last name')
        self.assertEqual(u._meta.get_field('phone').verbose_name,'phone')
        self.assertEqual(u._meta.get_field('join_date').verbose_name,'join date')
        self.assertEqual(u._meta.get_field('is_active').verbose_name,'is active')
        self.assertEqual(u._meta.get_field('is_staff').verbose_name,'is staff')
        self.assertEqual(u._meta.get_field('user_type').verbose_name,'user type')
        self.assertEqual(u._meta.get_field('is_for_testing').verbose_name,'is for testing')
        self.assertEqual(u._meta.get_field('gender').verbose_name,'gender')
                
        fields = ([field.name for field in get_user_model()._meta.fields])
        
        self.assertEqual(len(fields), 15)

    def test_user_fields_after_it_has_been_created(self):
        """
        User fields
        
        Ensure a user has the right fields after it has been created
        """
        u = get_user_model().objects.get(email='john@gmail.com')
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(str(u), 'john@gmail.com')
        self.assertEqual(u.email, 'john@gmail.com')
        self.assertEqual(u.first_name, 'John')
        self.assertEqual(u.last_name, 'Lock')
        self.assertEqual(u.phone, 254710223322)
        self.assertEqual(u.user_type, ADMIN_USER)
        self.assertEqual(u.is_for_testing, False)
        self.assertEqual(u.gender, 0)
        self.assertEqual((u.join_date).strftime("%B, %d, %Y"), today)
        self.assertEqual(u.is_active, True)
        self.assertEqual(u.is_staff, False)

    def test_get_short_name_method(self):
        u = get_user_model().objects.get(email='john@gmail.com')

        self.assertEqual(u.get_short_name(), 'John')

    def test_get_full_name_method(self):
        u = get_user_model().objects.get(email='john@gmail.com')

        self.assertEqual(u.get_full_name(), 'John Lock')

    def test_get_join_date_method(self):
        u = get_user_model().objects.get(email='john@gmail.com')

        # Check if get_created_date is correct
        self.assertTrue(DateUtils.do_created_dates_compare(
            u.get_join_date(u.get_user_timezone()))
        )

    def test_get_profile_image_url_method(self):
        
        ADMIN_USER = Profile.objects.get(user__email='john@gmail.com')
    
        # Test get_profile_image_url method for Top user
        self.assertEqual(ADMIN_USER.user.get_profile_image_url(),'/media/images/no_image.jpg')

    def test_get_profile_reg_no_method(self):

        ADMIN_USER = Profile.objects.get(user__email='john@gmail.com')
        
        # Test get_profile_reg_no method for Top user
        self.assertEqual(ADMIN_USER.user.get_profile_reg_no(), ADMIN_USER.reg_no)
        
    def test_if_create_ADMIN_USER_addittional_models_signal(self):
        """
    
        Ensure the signal creates profile, my settings and user's user groups
        """        
        u = get_user_model().objects.get(email='john@gmail.com')
        
        p = Profile.objects.get(user__email='john@gmail.com')
        
        # Check if profile reg_no matches with that of it's user
        self.assertEqual(p.reg_no, u.reg_no)
        
        """
        Check if MySetting is is created
        """        
        self.assertEqual(MySetting.objects.filter(name='main').count(), 1)
        self.assertEqual(MySetting.objects.all().count(), 1)

    
    def test_what_happens_when_a_user_is_deleted(self):
        
        # Confirm the existence of a user and profile
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(Profile.objects.all().count(), 1)
        
        # Now delete the user
        user = get_user_model().objects.get(email='john@gmail.com')
        user.delete()
        
        # Confrim if the user and profiles were both deleted
        self.assertEqual(get_user_model().objects.all().count(), 0)
        self.assertEqual(Profile.objects.all().count(), 0)
    
    def test_if_each_user_gets_a_group_with_their_email_as_name(self):

        # Create new user
        create_new_user('jack') 

        user1 = get_user_model().objects.get(email='john@gmail.com')
        self.assertEqual(
            user1.groups.all()[0], 
            Group.objects.get(name=user1.email)
        )

        user2 = get_user_model().objects.get(email='jack@gmail.com')
        self.assertEqual(
            user2.groups.all()[0], 
            Group.objects.get(name=user2.email)
        )




"""
=========================== UserManager ===================================
"""
# User
class UserManagerTestCase(TestCase):
 
    def test_UserManager_create_user_method(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_user method is working correctly
        """
        get_user_model().objects.create_user(
            email='john@gmail.com', 
            first_name='John', 
            last_name='Lock', 
            phone='254710223322',
            user_type=ADMIN_USER,
            gender=0,
            password='secretpass'
        )

        u = get_user_model().objects.get(email='john@gmail.com')
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(u.email, 'john@gmail.com')
        self.assertEqual(u.first_name, 'John')
        self.assertEqual(u.last_name, 'Lock')
        self.assertEqual(u.phone, 254710223322)
        self.assertEqual(u.user_type, ADMIN_USER)
        self.assertEqual(u.gender, 0)
        self.assertEqual(u.is_superuser, False)
        self.assertEqual((u.join_date).strftime("%B, %d, %Y"), today)
        self.assertEqual(u.is_active, True)
        self.assertEqual(u.is_staff, False)

    def test_if_UserManager_create_user_method_can_raise_email_error(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod can raise email error
        """
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='', 
                first_name='John', 
                last_name='Lock', 
                phone='254710223322',
                user_type=ADMIN_USER,
                gender=0,
                password='secretpass'
            )
            
    def test_device_UserManager_create_user_method_can_raise_first_name_error(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod can raise first_name error
        """
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='john@gmail.com', 
                first_name='', 
                last_name='Lock', 
                phone='254710223322',
                user_type=ADMIN_USER,
                gender=0,
                password='secretpass'
            )
            
    def test_device_UserManager_create_user_method_can_raise_last_name_error(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod can raise last_name error
        """
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='john@gmail.com', 
                first_name='John', 
                last_name='', 
                phone='254710223322',
                user_type=ADMIN_USER,
                gender=0,
                password='secretpass'
            )
            
    def test_device_UserManager_create_user_method_can_raise_phone_error(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod can raise phone error
        """
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='john@gmail.com', 
                first_name='John', 
                last_name='Lock', 
                phone='',
                user_type=ADMIN_USER,
                gender=0,
                password='secretpass'
            )
            
    def test_device_UserManager_can_create_superuser_method(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod is working correctly
        """
        get_user_model().objects.create_superuser(
            email='john@gmail.com', 
            first_name='John', 
            last_name='Lock', 
            phone='254710223322',
            gender=0,
            password='secretpass'
        )
        
        u = get_user_model().objects.get(email='john@gmail.com')
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(u.email, 'john@gmail.com')
        self.assertEqual(u.first_name, 'John')
        self.assertEqual(u.last_name, 'Lock')
        self.assertEqual(u.phone, 254710223322)
        self.assertEqual(u.user_type, ADMIN_USER)
        self.assertEqual(u.gender, 0)
        self.assertEqual(u.is_superuser, True)
        self.assertEqual((u.join_date).strftime("%B, %d, %Y"), today)
        self.assertEqual(u.is_active, True)
        self.assertEqual(u.is_staff, True)
        
    def test_device_UserManager_cant_create_a_user_with_an_non_unique_email(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod cant create a user with a non unique email
        """
        get_user_model().objects.create_user(email='john@gmail.com', 
                            first_name='John', 
                            last_name='Lock', 
                            phone='254710223322',
                            user_type=ADMIN_USER,
                            gender=0,
                            password='secretpass')
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                get_user_model().objects.create_user(email='john@gmail.com', 
                            first_name='John2', 
                            last_name='Lock2', 
                            phone='254711223322',
                            user_type=ADMIN_USER,
                            gender=0,
                            password='secretpass')
        
        
        self.assertEqual(get_user_model().objects.filter(email='john@gmail.com').count(), 1)
     
    
    def test_device_UserManager_cant_create_a_user_with_an_non_unique_phone(self):
        """
        UserManager's create_user method
        
        Ensure UserManager's create_usermethod cant create a user with a non unique phone
        """
        get_user_model().objects.create_user(
            email='john@gmail.com', 
            first_name='John', 
            last_name='Lock', 
            phone='254710223322',
            user_type=ADMIN_USER,
            gender=0,
            password='secretpass')
        
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                get_user_model().objects.create_user(
                    email='doe@gmail.com', 
                    first_name='Joe', 
                    last_name='Doe', 
                    phone='254710223322',
                    user_type=ADMIN_USER,
                    gender=0,
                    password='secretpass'
                )
        
        self.assertEqual(get_user_model().objects.filter(email='john@gmail.com').count(), 1)

"""
=========================== User methods ===================================
"""
class CreateUsersMethodTestCase(TestCase):

    def setUp(self):
        
        # Test if testing user is created successfully
        create_app_initial_users() 

    def test_verbose_names(self):
        u = get_user_model().objects.get(email='testing@gmail.com')

        self.assertEqual(u._meta.get_field('email').verbose_name,'email')
        self.assertEqual(u._meta.get_field('first_name').verbose_name,'first name')
        self.assertEqual(u._meta.get_field('last_name').verbose_name,'last name')
        self.assertEqual(u._meta.get_field('phone').verbose_name,'phone')
        self.assertEqual(u._meta.get_field('join_date').verbose_name,'join date')
        self.assertEqual(u._meta.get_field('is_active').verbose_name,'is active')
        self.assertEqual(u._meta.get_field('is_staff').verbose_name,'is staff')
        self.assertEqual(u._meta.get_field('user_type').verbose_name,'user type')
        self.assertEqual(u._meta.get_field('is_for_testing').verbose_name,'is for testing')
        self.assertEqual(u._meta.get_field('gender').verbose_name,'gender')
                
        fields = ([field.name for field in get_user_model()._meta.fields])
        
        self.assertEqual(len(fields), 15)


    def test_user_fields_after_it_has_been_created(self):
        """
        User fields
        
        Ensure a user has the right fields after it has been created
        """
        u = get_user_model().objects.get(email='testing@gmail.com')
        
        today = (timezone.now()).strftime("%B, %d, %Y")
    
        self.assertEqual(str(u), 'testing@gmail.com')
        self.assertEqual(u.email, 'testing@gmail.com')
        self.assertEqual(u.first_name, 'Just For')
        self.assertEqual(u.last_name, 'Testing')
        self.assertEqual(u.phone, 254720113322)
        self.assertEqual(u.user_type, EMPLOYEE_USER)
        self.assertEqual(u.is_for_testing, True)
        self.assertEqual(u.gender, 0)
        self.assertEqual((u.join_date).strftime("%B, %d, %Y"), today)
        self.assertEqual(u.is_active, True)
        self.assertEqual(u.is_staff, False)
        
    def test_if_create_app_initial_users_method_can_be_called_multiple_times_without_an_error(self):
        
        create_app_initial_users() 
        create_app_initial_users() 
        create_app_initial_users() 

        self.assertEqual(get_user_model().objects.all().count(), 1)
'''