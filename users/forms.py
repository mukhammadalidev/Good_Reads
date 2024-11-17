from django import forms
from django.core.mail import send_mail

# class UserCreateForm(forms.Form):
#     username = forms.CharField(max_length=200)
#     first_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=128)
from users.models import CustomUser


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        # if user.email:
        #     send_mail(
        #         "Welcome Goodreads Clone",
        #         "bu sayt shamsidinov Muhammadali tomonidan qurilgan",
        #         "mukhammadalidev@gmail.com",
        #         [user.email]
        #     )



class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','profile_picture')