import httpx
from mbb.moex.models import SecurityItem


def fetch_securities():
    columns = SecurityItem.model_fields.keys()
    columns_query_value = ",".join(x.upper() for x in columns)
    url = "https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?" \
          "iss.meta=off&iss.only=securities&"\
          f"securities.columns={columns_query_value}"

    with httpx.Client(verify=False) as client:
        response = client.get(url)
        data = response.json()
        return (SecurityItem(**dict(zip(columns, row))) for row in data["securities"]["data"])
