from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import MyLoginView

app_name = 'accounts'
urlpatterns = [
    path('accounts/login/', MyLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
