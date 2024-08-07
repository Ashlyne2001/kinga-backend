ADMIN_USER = 200000000 # Thsi will make it harder for an attacker to guess
DRIVER_USER = 1
CUSTOMER_USER = 2

USER_TYPE_CHOICES =[
    (ADMIN_USER, 'admin',),
    (DRIVER_USER, 'Driver',),   
    (CUSTOMER_USER, 'Customer',),
]

USER_GENDER_CHOICES =[
    (0, 'Male',),
    (1, 'Female',), 
    (2, 'Other',),  
]