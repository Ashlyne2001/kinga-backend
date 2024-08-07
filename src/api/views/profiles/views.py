
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics


from profiles.models import Customer, Driver
from api.serializers import (
    CustomerViewSerializer,
    DriverViewSerializer,
)

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerViewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ 
        For UX logger to work, the model should be stored in a variable
        named "self.obj" in the view instance
        """

        queryset = self.filter_queryset(self.get_queryset())

        # Get the single item from the filtered queryset
        self.obj = get_object_or_404(queryset)

        # May raise a permission denied
        self.check_object_permissions(self.request, self.obj)

        return self.obj

    def get_queryset(self):
        """
        Make sure only the owner can view his/her profile 
        """
        queryset = super(CustomerProfileView, self).get_queryset()
        queryset = queryset.filter(user__email=self.request.user)

        return queryset
    
class DriverProfileView(generics.RetrieveUpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverViewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ 
        For UX logger to work, the model should be stored in a variable
        named "self.obj" in the view instance
        """

        queryset = self.filter_queryset(self.get_queryset())

        # Get the single item from the filtered queryset
        self.obj = get_object_or_404(queryset)

        # May raise a permission denied
        self.check_object_permissions(self.request, self.obj)

        return self.obj

    def get_queryset(self):
        """
        Make sure only the owner can view his/her profile 
        """
        queryset = super(DriverProfileView, self).get_queryset()
        queryset = queryset.filter(user__email=self.request.user)

        return queryset
