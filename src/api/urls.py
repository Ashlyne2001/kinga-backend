from django.conf import settings
from django.urls import path

from api import views


'''
https://ef01-41-90-186-128.eu.ngrok.io/account_balance/queue/
'''


app_name = 'api'
urlpatterns = [

    
    path('api/api-token-auth/', views.TokenView.as_view(), name='token'),
    
    path('api/api-token-auth/',
         views.TokenView.as_view(), name='token_pos'),
    path('api/signup/', views.SignupView.as_view(), name='signup'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    
    path(
        'api/customer/profile/', 
        views.CustomerProfileView.as_view(), 
        name='customer_profile'
    ),
    path(
        'api/driver/profile/', 
        views.DriverProfileView.as_view(), 
        name='driver_profile'
    ),

    path(
        'api/trips/',
        views.TripIndexView.as_view(),
        name='trip_index'
    ),

    

   






   

    
    


   
    
  

    
   

    
    

   

    








    # TimsReceiptUpdateView

   
   
]
