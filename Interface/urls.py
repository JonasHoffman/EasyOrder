from django.urls import path
from Interface import views


app_name = "interface"


urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.homeinicial, name="homeinicial"),
    path("minhaloja", views.homeDiagrama, name="minhaloja"),

]