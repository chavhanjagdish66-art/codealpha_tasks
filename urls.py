from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth

urlpatterns = [
    path('admin/', admin.site.urls),

    # store app
    path('', include('store.urls')),

    # login logout
    path('accounts/login/', auth.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('accounts/logout/', auth.LogoutView.as_view(next_page='/'), name='logout'),
]