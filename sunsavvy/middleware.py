# myapp/middleware.py

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect

class PasswordProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.password = getattr(settings, 'PASSWORD', 'default_password')

    def __call__(self, request):
        if not request.session.get('authenticated'):
            if request.path != '/' and not request.POST.get('password') == self.password:
                return redirect('login')
        response = self.get_response(request)
        return response