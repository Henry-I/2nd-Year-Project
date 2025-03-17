from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from .forms import UserChangeForm, CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        customer_group, created = Group.objects.get_or_create(name='Customer')
        self.object.groups.add(customer_group)

        login(self.request, self.object)

        return response

class UpdateProfileView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'registration/update_profile.html'
    success_url = reverse_lazy('accounts:update_profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class DeleteProfileView(View):
    def get(self, request):
        return render(request, 'registration/delete_profile.html')
