from channels.sessions import CookieMiddleware, SessionMiddleware
from channels.auth import AuthMiddleware

"""    
Handy shortcut for applying all three layers at once 
We found it from channels.auth import AuthMiddleware

Our cutstom 'TokenAuthMiddlewareStack' is imported and used in .asgi
"""
# Handy shortcut for applying all three layers at once
def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(AuthMiddleware(inner)))