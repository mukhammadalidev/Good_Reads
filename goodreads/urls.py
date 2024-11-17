from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .view import landing,HomePageView
urlpatterns = [
    path('',landing,name="landing"),
    path('users/',include('users.urls')),
    path('books/',include('books.urls')),
    path('home/',HomePageView,name='home'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)