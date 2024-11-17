from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Register,Login,Profile,LogoutView,ProfileUpdateView
app_name = 'users'
urlpatterns = [
    path('register',Register.as_view(),name="register"),
    path('login',Login.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('profile/edit/',ProfileUpdateView.as_view(),name="profile-edit"),
    path('profile/',Profile.as_view(),name="profile")
]

