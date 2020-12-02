from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('taketest/', views.taketest, name='taketest'),
    
    path('account/', include('account.urls')),
]
