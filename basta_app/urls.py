"""basta_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .views import SignupView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += i18n_patterns(
    path('', include("basta.urls", namespace="basta")),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path(
        'accounts/password/reset/',
        auth_views.password_reset,
        {
        'post_reset_redirect': reverse('auth_password_reset_done'),
        'html_email_template_name': 'registration/password_reset_html_email.html'
        },
        name='auth_password_reset'
    ),
    path('accounts/', include('django.contrib.auth.urls')),
)