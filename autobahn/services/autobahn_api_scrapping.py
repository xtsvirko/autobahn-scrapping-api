import asyncio
from typing import List
import httpx
import requests

from app.settings import BASE_AUTOBAHN_API_URL
from autobahn.models import Road, Roadwork


async def fetch_json(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


async def scrape_roads(client: httpx.AsyncClient, url: str) -> List[Road]:
    roads_response = await fetch_json(client, url)
    return [Road(road_id=road) for road in roads_response.get("roads", [])]


async def scrape_roadworks_in_road(
    client: httpx.AsyncClient, road: Road, base_api_url: str
) -> List[Roadwork]:
    url = f"{base_api_url}/{road.road_id}/services/roadworks"
    roadworks_response = await fetch_json(client, url)
    return [
        Roadwork(
            identifier=rw.get("identifier"),
            extent=rw.get("extent"),
            is_blocked=rw.get("isBlocked") is True,
            title=rw.get("title"),
            road=road,
        )
        for rw in roadworks_response.get("roadworks", [])
    ]


async def scrape_all_roadworks(
    base_api_url: str = BASE_AUTOBAHN_API_URL,
) -> List[Roadwork]:
    async with httpx.AsyncClient() as client:
        roads = await scrape_roads(client, base_api_url)
        tasks = [scrape_roadworks_in_road(client, road, base_api_url) for road in roads]
        results = await asyncio.gather(*tasks)
        return [rw for sublist in results for rw in sublist]


def save_roadworks(roadworks: List[Roadwork]) -> None:
    for roadwork in roadworks:
        if not roadwork.road.pk:
            roadwork.road.save()
        roadwork.save()


def sync_roadworks_with_api():
    roadworks = asyncio.run(scrape_all_roadworks(BASE_AUTOBAHN_API_URL))
    save_roadworks(roadworks)
