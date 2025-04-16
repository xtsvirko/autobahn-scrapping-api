from typing import List

import requests

from app.settings import BASE_AUTOBAHN_API_URL
from autobahn.models import Road, Roadwork

# BASE_AUTOBAHN_API_URL = "https://verkehr.autobahn.de/o/autobahn"


def scrape_roads(base_api_url: str = BASE_AUTOBAHN_API_URL) -> List[Road]:
    api_url = base_api_url
    roads_response = requests.get(api_url).json()
    roads = []
    for road in roads_response.get("roads"):
        roads.append(Road(road_id=road))
    return roads


def scrape_roadworks_in_road(
    road: Road,
    base_api_url: str = BASE_AUTOBAHN_API_URL,
) -> List[Roadwork]:
    road_id = road.road_id
    roadworks_url = f"{base_api_url}/{road_id}/services/roadworks"
    roadworks_response = requests.get(roadworks_url).json()
    roadworks = []
    for roadwork in roadworks_response.get("roadworks"):
        roadworks.append(
            Roadwork(
                identifier=roadwork.get("identifier"),
                extent=roadwork.get("extent"),
                is_blocked=roadwork.get("isBlocked") is True,
                title=roadwork.get("title"),
                road=road,
            )
        )
    return roadworks


def scrape_all_roadworks(base_api_url: str = BASE_AUTOBAHN_API_URL) -> List[Roadwork]:
    roadworks = []
    roads = scrape_roads(base_api_url)
    for road in roads:
        roadworks.extend(scrape_roadworks_in_road(road))
    return roadworks


def save_roadworks(roadworks: List[Roadwork]) -> None:
    for roadwork in roadworks:
        if not roadwork.road.pk:
            roadwork.road.save()
        roadwork.save()


def sync_roadworks_with_api():
    roadworks = scrape_all_roadworks(BASE_AUTOBAHN_API_URL)
    save_roadworks(roadworks)
