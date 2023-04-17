from django.urls import path
#from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(r'service/', views.service, name='service'),
    path(r'log/', views.log, name='log'),
    path('', views.index, name='index'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)