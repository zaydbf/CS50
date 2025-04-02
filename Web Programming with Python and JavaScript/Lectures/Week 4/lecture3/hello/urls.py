from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"), # "" means the default page views.index what I want to show(render) name is the name of the path(makes it easy to reference in other apps)
    path("brian", views.brian, name="brian"), #brian is what comes after the /hello ( so I need to put 127.0.0.1:8000/hello/brian)
    path("david", views.david, name="david"),
    path("<str:name>", views.greet, name="greet") #make the process general so the path is hello/(a given name) greet will be rendered
]