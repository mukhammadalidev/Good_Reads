from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from django.shortcuts import render, redirect
from .forms import UserCreateForm, UserLoginForm, UserProfileForm
# Create your views here.
from django.views import View


class Register(View):
    def get(self,request):
        create_form = UserCreateForm()
        context = {
            "form":create_form
        }
        return render(request,'register.html',context)

    def post(self,request):
        user_create = UserCreateForm(data=request.POST)
        if user_create.is_valid():
            user_create.save()
            return redirect('users:login')
        else:
            context = {
                "form": user_create
            }
            return render(request, 'register.html', context)





class Login(View):
    def get(self,request):
        user_login = AuthenticationForm()
        return render(request,'login.html',{'form':user_login})
    def post(self,request):
        user_form = AuthenticationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.get_user()
            login(request,user)
            messages.success(request, "You have successfully logged in.")

            return redirect('landing')
        else:
            return render(request, 'login.html', {'form': user_form})


class Profile(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'profile.html',{"user":request.user})



class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.info(request,"You have successfully logged out.")
        return redirect("landing")

class ProfileUpdateView(LoginRequiredMixin,View):
    def get(self,request):
        user_profile_form = UserProfileForm(instance=request.user)

        return render(request,'profile_edit.html',{"form":user_profile_form})
    def post(self,request):
        user_profile_form = UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)

        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.success(request,"Your profile success updated.")
            return redirect("users:profile")
        else:
            return render(request,'profile_edit.html',{"form":user_profile_form})
