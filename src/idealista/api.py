import attr
from functools import lru_cache
import logging
from typing import List, Dict, Union, Optional, Any

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

from .enums import PropertyType, SinceDate, Sort, Operation

logger = logging.getLogger(__name__)


TOKEN_URL = "https://api.idealista.com/oauth/token"
API_URL_TEMPLATE = "https://api.idealista.com/3.5/{country}/search"


@attr.s(kw_only=True, auto_attribs=True)
class Point:
    latitude: float = attr.ib()
    longitude: float = attr.ib()

    def __str__(self):
        return f"{self.latitude},{self.longitude}"


@lru_cache()
def get_token(client_id, client_secret):
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=TOKEN_URL, auth=auth)
    return token


def _prepare_location_data(
    center: Optional[str] = None,
    distance: Optional[float] = None,
    location_id: Optional[str] = None,
) -> Dict[str, Any]:
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


def _prepare_extra_data(**kwargs: Any) -> Dict[str, Any]:
    return {key: value for key, value in kwargs.items() if value is not None}


def prepare_data(
    country: str,
    operation: str,
    property_type: str,
    center: Optional[str] = None,
    distance: Optional[float] = None,
    location_id: Optional[str] = None,
    **kwargs: Union[str, bool, float, List[int], None],
) -> Dict[str, Union[str, bool, float]]:
    base_data = {
        "country": country,
        "operation": operation,
        "propertyType": PropertyType(property_type).value,
    }
    location_data = _prepare_location_data(center, distance, location_id)
    extra_data = _prepare_extra_data(**kwargs)

    # https://www.python.org/dev/peps/pep-0584/#d1-d2
    data = {**base_data, **location_data, **extra_data}
    return data


@attr.s(auto_attribs=True)
class Idealista:
    client_id: str = attr.ib()
    token: Dict[str, Union[str, int]] = attr.ib()

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
        center: Optional[Point] = None,
        locale: Optional[str] = None,
        distance: Optional[float] = None,
        location_id: Optional[str] = None,
        max_items: Optional[int] = None,
        num_page: Optional[int] = None,
        max_price: Optional[float] = None,
        min_price: Optional[float] = None,
        since_date: Optional[SinceDate] = None,
        order: Optional[str] = None,
        sort: Optional[Sort] = None,
        ad_ids: Optional[List[int]] = None,
        has_multimedia: Optional[bool] = None,
    ) -> Any:
        api_url = API_URL_TEMPLATE.format(country=country)
        data = prepare_data(
            country,
            Operation(operation).value if operation is not None else operation,
            PropertyType(property_type).value
            if property_type is not None
            else property_type,
            str(center) if center is not None else center,
            distance,
            location_id,
            locale=locale,
            max_items=max_items,
            num_page=num_page,
            max_price=max_price,
            min_price=min_price,
            since_date=SinceDate(since_date).value
            if since_date is not None
            else since_date,
            order=order,
            sort=Sort(sort).value if sort is not None else sort,
            ad_ids=ad_ids,
            has_multimedia=has_multimedia,
        )

        response = self.client.post(api_url, data=data)
        response.raise_for_status()

        return response.json()
