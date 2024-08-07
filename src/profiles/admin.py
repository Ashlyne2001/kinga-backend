from django.contrib import admin
from profiles.forms import ProfileAdminForm

from profiles.models import Customer, Driver, Profile

class ProfileAdmin(admin.ModelAdmin):

    form = ProfileAdminForm

    date_hierarchy = 'join_date'
    empty_value_display = '-empty-'
    readonly_fields = ('user', 'join_date', 'reg_no',)

    fieldsets = [
            (None, {'fields': (
                'user',
                'join_date', 
                'phone',
                )})]

    list_display = ('get_full_name', 'user', 'reg_no', 'get_admin_join_date', )
    list_filter = ['join_date']

    def get_actions(self, request):
        """ Disable delete_selected action from this admin """
        actions = super().get_actions(request)

        # Show make payment actions
        self.show_make_payment_actions(request)
     
        return actions

    def show_make_payment_actions(self, request):
        """ Only show make payment options to superuser """

        if request.user.is_superuser:

            # This actions have been provided by ProfileAdminPaymentActionMixin
            payment_actions = [
                'make_payment_for_1_month', 
                'make_payment_for_6_months', 
                'make_payment_for_1_year']

            self.actions = self.actions + payment_actions

        else:
            # To avoid the django admin cache, we empty actions when we are not
            # supposed to show any
            self.actions = []

        return False

    # def has_delete_permission(self, request, obj=None):
    #     """ Disable delete button/action from this admin """
    #     return True

    # def has_add_permission(self, request):
    #     """ Disable add button/action from this admin """
    #     return False

admin.site.register(Profile, ProfileAdmin)

class CustomerAdmin(admin.ModelAdmin):
    ordering = ('user__first_name',)
    list_display = ('__str__', 'phone',)
    fieldsets = []

admin.site.register(Customer, CustomerAdmin)



class DriverAdmin(admin.ModelAdmin):
    ordering = ('user__first_name',)
    list_display = ('__str__', 'phone', )
    fieldsets = []

admin.site.register(Driver, DriverAdmin)
