from django.contrib.auth.backends import ModelBackend
from drawer.models import Token


class TokenBackend(ModelBackend):
    '''
    Possibly the worst authentication backend ever.
    Looks for a token, if found returns user attached.
    '''

    def authenticate(self, token=None):
        try:
            return Token.objects.get(token=token).user
        except Token.DoesNotExist:
            return None
        except Token.MultipleObjectsReturned:
            raise Exception("Multiple tokens returned.")
