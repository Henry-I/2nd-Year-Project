from django.urls import path
from .views import SignUpView, UpdateProfileView, DeleteProfileView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('delete_profile/', DeleteProfileView.as_view(), name='delete_profile'),
] 