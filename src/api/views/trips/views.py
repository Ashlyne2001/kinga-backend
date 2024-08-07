from rest_framework import generics
from rest_framework import permissions
from accounts.utils.user_type import DRIVER_USER, CUSTOMER_USER

from api.serializers import TripListSerializer
from api.utils.api_pagination import StandardResultsSetPagination

from trips.models import Trip


class TripIndexView(generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Make sure only the owner can view his/her store

        Returns all products excluding variant and bundle parents
        """
        queryset = super(TripIndexView, self).get_queryset()

        # Check if user is driver or customer and filter accordingly
        if self.request.user.user_type == DRIVER_USER:
            queryset = queryset.filter(driver__user=self.request.user)

        elif self.request.user.user_type == CUSTOMER_USER:
            queryset = queryset.filter(customer__user=self.request.user)

        queryset = queryset.filter().order_by('-id')

        return queryset