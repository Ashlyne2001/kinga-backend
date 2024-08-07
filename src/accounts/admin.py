from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from accounts.models import GroupProxy, UserGroup


from .forms import UserCreationAdminForm

# Register your models here.

admin.site.site_header  =  "Kinga Admin Site"  
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationAdminForm

    readonly_fields = ('get_user_type',)
        
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'first_name', 
        'last_name', 
        'email', 
        'phone', 
        'user_type', 
        'reg_no', 
        'is_for_testing',
        'is_staff', 
        'is_active')
    list_filter = ('is_staff','user_type')
    fieldsets = (
            ('Personal info', {'fields': (
                'first_name', 
                'last_name', 
                'email', 
                'get_user_type',
                'is_for_testing',
                'gender')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'groups')}),
            )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
            (None, {
                    'classes': ('wide',),
                    'fields': (
                        'first_name', 
                        'last_name', 
                        'email', 
                        'phone', 
                        'user_type', 
                        'gender', 
                        'password1', 
                        'password2')}
    ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    actions = [
        'create_profile_if_missing'
    ]

    def get_user_type(self, obj):
        return get_user_model().USER_TYPE_CHOICES[obj.user_type][1].title()
    get_user_type.short_description = "User type"

    @admin.action(description='Create profile')
    def create_profile_if_missing(self, request, queryset):
        for q in queryset:
            q.create_profile_if_missing()

admin.site.register(get_user_model(), UserAdmin)


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('ident_name', 'reg_no')

admin.site.register(UserGroup, UserGroupAdmin)



class GroupProxyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_all_perms')

    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

admin.site.register(GroupProxy, GroupProxyAdmin)