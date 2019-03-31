from django.urls import include, path

urlpatterns = [
    path('accounts/', include('nopassword.urls')),
]
