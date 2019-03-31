from nopassword.views import LoginView


class AdminLoginView(LoginView):
    template_name = 'nopassword_admin/login.html'
