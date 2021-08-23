# python-idealista documentation

python-idealista is a Python library to interact with the Idealista API.

## Usage

Example usage:

```python
import os

from idealista import Idealista, PropertyType, Operation, SinceDate


client_id = os.environ["IDEALISTA_CLIENT_ID"]
client_secret = os.environ["IDEALISTA_CLIENT_SECRET"]

api = Idealista.authenticate(client_id, client_secret)

result = api.search(
    location_id="0-EU-ES-28",
    country="es",
    max_items=50,
    num_page=1,
    property_type=PropertyType.HOMES,
    operation=Operation.RENT,
    max_price=1000,
    since_date=SinceDate.LAST_WEEK,
)
print(result)
```
