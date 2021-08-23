from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

import attr
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from .enums import Operation, PropertyType, SinceDate, Sort

logger = logging.getLogger(__name__)


TOKEN_URL = "https://api.idealista.com/oauth/token"
API_URL_TEMPLATE = "https://api.idealista.com/3.5/{country}/search"


@attr.define(kw_only=True)
class Point:
    latitude: float
    longitude: float

    def __str__(self):
        return f"{self.latitude},{self.longitude}"


@lru_cache
def get_token(client_id, client_secret):
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TOKEN_URL, auth=auth)
    return token


def _prepare_location_data(
    center: str | None = None,
    distance: float | None = None,
    location_id: str | None = None,
) -> dict[str, Any]:
    if (center is None and distance is None and location_id is None) or (
        center is not None and distance is not None and location_id is not None
    ):
        raise ValueError(
            "You must specify a center + distance or locationId in each request"
        )
    elif center is not None and distance is not None:
        location_data = {
            "center": center,
            "distance": distance,
        }
    else:
        location_data = {"locationId": location_id}

    return location_data


def _prepare_extra_data(**kwargs: Any) -> dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}


def prepare_data(
    country: str,
    operation: str,
    property_type: str,
    center: str | None = None,
    distance: float | None = None,
    location_id: str | None = None,
    **kwargs: str | bool | float | list[int] | None,
) -> dict[str, str | bool | float]:
    base_data = {
        "country": country,
        "operation": operation,
        "propertyType": PropertyType(property_type).value,
    }
    location_data = _prepare_location_data(center, distance, location_id)
    extra_data = _prepare_extra_data(**kwargs)

    # https://www.python.org/dev/peps/pep-0584/#d1-d2
    data = base_data | location_data | extra_data
    return data


@attr.define
class Idealista:
    client_id: str
    token: dict[str, str | int]

    @classmethod
    def authenticate(cls, client_id, client_secret):
        token = get_token(client_id, client_secret)
        logger.debug("Token: %s", token)
        return cls(client_id, token)

    @property
    def client(self):
        client = OAuth2Session(self.client_id, token=self.token)
        return client

    def search(
        self,
        country: str,
        operation: Operation,
        property_type: PropertyType,
        center: Point | None = None,
        locale: str | None = None,
        distance: float | None = None,
        location_id: str | None = None,
        max_items: int | None = None,
        num_page: int | None = None,
        max_price: float | None = None,
        min_price: float | None = None,
        since_date: SinceDate | None = None,
        order: str | None = None,
        sort: Sort | None = None,
        ad_ids: list[int] | None = None,
        has_multimedia: bool | None = None,
    ) -> Any:
        api_url = API_URL_TEMPLATE.format(country=country)

        operation_str = (
            Operation(operation).value if operation is not None else operation
        )
        property_type_str = (
            PropertyType(property_type).value
            if property_type is not None
            else property_type
        )
        center_str = str(center) if center is not None else center
        since_date_str = (
            SinceDate(since_date).value if since_date is not None else since_date
        )
        sort_str = Sort(sort).value if sort is not None else sort

        data = prepare_data(
            country,
            operation_str,
            property_type_str,
            center_str,
            distance,
            location_id,
            locale=locale,
            max_items=max_items,
            num_page=num_page,
            max_price=max_price,
            min_price=min_price,
            since_date=since_date_str,
            order=order,
            sort=sort_str,
            ad_ids=ad_ids,
            has_multimedia=has_multimedia,
        )

        response = self.client.post(api_url, data=data)
        response.raise_for_status()

        return response.json()
