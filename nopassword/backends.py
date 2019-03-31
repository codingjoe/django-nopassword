from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.signing import BadSignature
from django.urls import reverse

from . import signing


class NoPasswordBackend(ModelBackend):
    signer = signing.UserSigner(sep='/')

    def authenticate(self, request, token=None):
        max_age = getattr(settings, 'NOPASSWORD_LOGIN_CODE_TIMEOUT', 900)

        try:
            user = self.signer.unsign(token, max_age=max_age)
        except (get_user_model().DoesNotExist, BadSignature):
            return
        else:
            if self.user_can_authenticate(user):
                return user

    @classmethod
    def get_token(cls, user):
        return cls.signer.sign(user)

    @staticmethod
    def get_login_url(token):
        return reverse(
            'nopassword:login-token',
            kwargs={'token': token}
        )
