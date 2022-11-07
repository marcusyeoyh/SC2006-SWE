"""django_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    #api urls
    path('api/search/', views.SearchView.as_view()),
    path('api/comparison/', views.ComparisonView.as_view()),
    path('api/likes/', views.UpdateLikesView.as_view()),
    #amenities urls
    path('api/airport/', views.Airport.as_view()),
    path('api/atm/', views.ATM.as_view()),
    path('api/buses/', views.Buses.as_view()),
    path('api/clinic/', views.Clinic.as_view()),
    path('api/grocery/', views.Grocery.as_view()),
    path('api/hospital/', views.Hospital.as_view()),
    path('api/mall/', views.Mall.as_view()),
    path('api/mrt/', views.MRT.as_view()),
    path('api/restaurant/', views.Restaurant.as_view()),
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
