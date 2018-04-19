"""workspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from tellme import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', views.index),
    re_path(r'^login/$', views.login_view),
    re_path(r'^logout/$', views.logout_view),
    re_path(r'^changepass/$', views.change_pass),
    re_path(r'^search/', views.search),
    re_path(r'^delete/(?P<url>\w+)/(?P<id>\w+)/$', views.delete),
    re_path(r'^jtid/(\d*)', views.jtid),
    re_path(r'^jtidadd/', views.jtid_add),
    re_path(r'^cid/(\d+)/', views.cid),
    re_path(r'^cidadd/', views.cid_add),
    re_path(r'^cidedit/(\d+)', views.cid_edit),
    re_path(r'^siteadd/(\d+)', views.site_add),
    re_path(r'^siteedit/(\d+\w+)', views.site_edit),
    re_path(r'^add/(?P<svc>\w+)/(?P<id>\w+)/$', views.svc_add),
    re_path(r'^edit/(?P<svc>\w+)/(?P<id>\w+)/$', views.svc_edit),
    re_path(r'^tag/(?P<svc>\w+)/(?P<id>\w+)/$', views.tag),
    re_path(r'^photo/(\w+)', views.photo),
    re_path(r'^report/(\w+)', views.report),
    re_path(r'^trashfile/(\w+)/(\d+)', views.trashfile),
    re_path(r'^history/', views.history),
]
