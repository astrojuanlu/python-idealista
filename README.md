# python-idealista

[![Documentation Status](https://readthedocs.org/projects/python-idealista/badge/?version=latest)](https://python-idealista.readthedocs.io/en/latest/?badge=latest)

python-idealista is a Python library to interact with the Idealista API.

## Usage

```python
import asyncio
import os

from idealista import Idealista, PropertyType, Operation, SinceDate


client_id = os.environ["IDEALISTA_CLIENT_ID"]
client_secret = os.environ["IDEALISTA_CLIENT_SECRET"]

async def main():
    api = await Idealista.authenticate(client_id, client_secret)

    result = await api.search(
        location_id="0-EU-ES-28",
        country="es",
        max_items=50,
        num_page=1,
        property_type=PropertyType.HOMES,
        operation=Operation.RENT,
        max_price=1000,
        since_date=SinceDate.LAST_WEEK,
    )
    return result

print(asyncio.run(main()))
```
