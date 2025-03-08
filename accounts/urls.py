from django.urls import path
from .views import SignUpView, UpdateProfileView, DeleteProfileView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'

urlpatterns = [
    path('create/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_profile'),
] 