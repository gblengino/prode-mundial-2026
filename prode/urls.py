from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("prode/", views.prode, name="prode"),
    path("clasificacion/", views.clasificacion, name="clasificacion"),
    path("register/", views.register, name='register')
]