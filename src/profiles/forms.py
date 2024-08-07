from PIL import Image, ExifTags

from django import forms
from django.contrib.auth import get_user_model

from profiles.models import Profile



User = get_user_model()



class ProfileAdminForm(forms.ModelForm):
    """ Add widget to fields """
    
 