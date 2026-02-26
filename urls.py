from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("core.urls")),
    path("accounts/login/",auth.LoginView.as_view(template_name="login.html")),
    path("accounts/logout/",auth.LogoutView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)