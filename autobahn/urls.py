from django.urls import path

from autobahn.views import RoadListView, RoadworkListView

app_name = "autobahn"

urlpatterns = [
    path("roads/", RoadListView.as_view(), name="road_list"),
    path("roadworks", RoadworkListView.as_view(), name="roadwork_list"),
]
