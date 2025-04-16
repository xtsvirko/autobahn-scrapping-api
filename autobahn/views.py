from django.shortcuts import render
from django.views import generic

from autobahn.models import Road, Roadwork


# Create your views here.
class RoadListView(generic.ListView):
    model = Road
    template_name = "autobahn/road_list.html"
    paginate_by = 5


class RoadworkListView(generic.ListView):
    model = Roadwork
    template_name = "autobahn/roadwork_list.html"
    paginate_by = 5
