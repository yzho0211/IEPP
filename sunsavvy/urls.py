from django.urls import path 
from . import views

#URL Config
urlpatterns = [
    path('', views.login_view, name= "login"),
    path('home/', views.home, name= "home"),
    # path('cloth_style/', views.cloth_style, name= "cloth_style"),
    path('sunscreen_safety/', views.sunscreen_safety, name= "sunscreen_safety"),
    path('uv_impact/', views.uv_impact, name= "uv_impact")
]
