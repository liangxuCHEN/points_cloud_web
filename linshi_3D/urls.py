"""linshi_3D URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from three_d import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^test_js/(?P<p_id>\d+)$', views.test_js, name='test_js'),
    url(r'^test_obj/(?P<p_id>\d+)$', views.test_obj, name='test_obj'),
    url(r'^admin/', admin.site.urls),

   url(r'^td_models$', views.TDModelIndexView.as_view(), name='tdmodel_index'),
   url(r'^obj_models$', views.ObjModelIndexView.as_view(), name='objmodel_index'),
   url(r'^upload_zip$', views.load_obj_zip, name='upload_zip'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

