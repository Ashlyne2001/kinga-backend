from django.contrib.auth.views import LoginView

from accounts.forms import MyAuthenticationForm

# pylint: disable = useless-super-delegation

class MyLoginView(LoginView):
    template_name = 'accounts/login_form.html' 
    form_class = MyAuthenticationForm
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        return super(MyLoginView, self).post(request, *args, **kwargs)
        
    def form_valid(self, form):
        return super(MyLoginView, self).form_valid(form)
    
    def form_invalid(self, form):
        return super(MyLoginView, self).form_invalid(form)
