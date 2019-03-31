import datetime

from django.contrib.auth import get_user_model
from django.core.signing import SignatureExpired
from django.test import TestCase

from nopassword import signing


class FrozenUserSigner(signing.UserSigner):
    """Freeze timestamp for test runs."""
    def timestamp(self):
        return '1Hjptg'


class TestUserSigner(TestCase):
    signature = 'LZ:173VAm:1Hjptg:vKf_ZeqHvcTlSozFOcVvuyZgJx8'

    def test_sign(self):
        user = get_user_model().objects.create_user(
            pk=1337,
            username='spidy',
            last_login=datetime.datetime(2002, 5, 3),
        )
        signer = FrozenUserSigner()
        signature = signer.sign(user)
        self.assertEqual(signature, self.signature)

    def test_unsign(self):
        user = get_user_model().objects.create_user(
            pk=1337,
            username='spiderman',
            last_login=datetime.datetime(2002, 5, 3),
        )
        signer = FrozenUserSigner()
        self.assertEqual(user, signer.unsign(self.signature))

    def test_unsign__no_user(self):
        signer = FrozenUserSigner()
        self.assertRaisesMessage(
            signing.UserDoesNotExist,
            "User with pk=1337 does not exist",
            signer.unsign, self.signature,
        )

    def test_unsign__last_login(self):
        get_user_model().objects.create_user(
            pk=1337,
            username='spiderman',
            # later date, that does not match the signature
            last_login=datetime.datetime(2012, 7, 3),
        )
        signer = FrozenUserSigner()
        self.assertRaisesMessage(
            SignatureExpired,
            "The access token for <CustomUser: spiderman> seems used",
            signer.unsign, self.signature,
        )

    def test_to_timestamp(self):
        value = datetime.datetime(2002, 5, 3)
        base62_value = signing.UserSigner.to_timestamp(value=value)
        self.assertEqual(base62_value, '173VAm')
