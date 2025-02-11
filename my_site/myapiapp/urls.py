from django.urls import path

from .views import hello_world_view, GroupsListApiView

app_name: str = "myapiapp"

urlpatterns = [
    path("hello/", hello_world_view, name="api_hello"),
    path("groups/", GroupsListApiView.as_view(), name="api_groups"),
]
