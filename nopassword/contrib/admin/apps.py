from django.apps import AppConfig


class NoPasswordAdmin(AppConfig):
    name = 'nopassword.contrib.admin'
    label = 'nopassword_admin'
    verbose_name = "noPassword admin"
