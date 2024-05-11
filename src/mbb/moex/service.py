import httpx
from mbb.moex.models import SecurityItem, SecurityMarketDataItem


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


def fetch_marketdata():
    columns = SecurityMarketDataItem.model_fields.keys()
    columns_query_value = ",".join(x.strip('_').upper() for x in columns)
    url = "https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?" \
          "iss.meta=off&iss.only=marketdata&"\
          f"marketdata.columns={columns_query_value}"

    def filter_item(item: SecurityMarketDataItem):
        return item.last is not None

    with httpx.Client(verify=False) as client:
        response = client.get(url)
        data = response.json()
        return (
            item for row in data["marketdata"]["data"]
            if filter_item(item := SecurityMarketDataItem(**dict(zip(columns, row))))
        )
