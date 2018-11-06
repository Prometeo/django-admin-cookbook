"""admin_cookbook URL Configuration

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
from django.contrib.auth.models import User, Group
from django.urls import path
from events.admin import event_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('entity-admin/', admin.site.urls),
    path('event-admin/', event_admin_site.urls),
]

# Both admins are available at their respective urls, /entity-admin/ and event-admin/.

admin.site.site_header = "UMSRA Admin"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Welcome to UMSRA Researcher Portal"

# Remove default apps from django admin
admin.site.unregister(User)
admin.site.unregister(Group)
