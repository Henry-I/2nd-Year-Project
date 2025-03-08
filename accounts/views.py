from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, UserChangeForm
from .models import CustomUser
from django.shortcuts import render
from django.views import View



class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)

        customer_group, created = Group.objects.get_or_create(name='Customer')
        self.object.groups.add(customer_group)

        login(self.request, self.object)
        
        return response 

class UpdateProfileView(UpdateView):
    model = CustomUser
    form_class = UserChangeForm
    template_name = 'registration/update_profile.html'


    def form_valid(self, form):
        response = super().form_valid(form)
        return(response)


class DeleteProfileView(View):
    def get(self, request):
        return render(request, 'registration/delete_profile.html')
