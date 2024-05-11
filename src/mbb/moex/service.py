from typing_extensions import List
import httpx
from mbb.moex.models import SecurityItem, SecurityMarketDataItem, SecuritySearchItem


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


def search_all(query: str = None):
    result = []
    limit = 100
    start = 0
    while True:
        part = search(query=query, start=start, limit=limit)
        print(part)
        result.extend(part)
        if len(part) < limit:
            break
        start = start + limit
    return result


def search(**kwargs):
    columns = list(SecuritySearchItem.model_fields.keys())
    with httpx.Client(verify=False) as client:
        url = make_search_url(**kwargs, columns = columns)
        print(url)
        response = client.get(url)
        data = response.json()
        return list(SecuritySearchItem(**dict(zip(columns, row))) for row in data["securities"]["data"])


def make_search_url(query: str = None, start=0, limit=100, columns: List = None):
    columns_query_value = ",".join(columns)
    url = f"https://iss.moex.com/iss/securities.json?iss.meta=off&engine=stock&market=bonds" \
        f"&securities.columns={columns_query_value}" \
        f"&is_trading=1" \
        f"{('&q=' + query) if query else ''}" \
        f"&start={start}&limit={limit}"
    return url
