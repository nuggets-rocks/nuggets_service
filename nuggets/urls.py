"""nuggets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.http import HttpResponse
from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login$', TemplateView.as_view(template_name='login.html')),
    url(r'^google5c17accd1a8ca615\.html$', lambda r: HttpResponse("google-site-verification: "
                                                                  "google5c17accd1a8ca615.html",
                                                                  mimetype="text/plain")),
    url(r'', include('nuggets_api.urls')),
]
