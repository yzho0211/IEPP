from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class DefaultPasswordBackend(BaseBackend):
    def authenticate(self, request, password=None):
        default_password = 'team22'
        if password == default_password:
            user, created = User.objects.get_or_create(username='default_user')
            if created:
                user.set_password(default_password)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None