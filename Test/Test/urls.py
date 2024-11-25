"""
URL configuration for Test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

def redirect_to_main(request):
    return redirect('main')

urlpatterns = [
    path('', redirect_to_main),
    path('admin/', admin.site.urls),
    path('', include('main.main_urls')),
    path('account', include('main.account_urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)