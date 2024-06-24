from typing_extensions import List, Union, Sequence
from contextlib import closing
import httpx
from pydantic import ValidationError
from mbb.moex.models import SecurityItem, SecurityMarketDataItem, SecuritySearchItem


def fetch_securities(connection) -> Sequence[Union[SecurityItem, None]]:
    columns = SecurityItem.model_fields.keys()
    columns_query_value = ",".join(x.upper() for x in columns)
    url = "https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?" \
          "iss.meta=off&iss.only=securities&"\
          f"securities.columns={columns_query_value}"

    def row_to_item(row):
        try:
            return SecurityItem(**dict(zip(columns, row)))
        except ValidationError:
            return None

    with httpx.Client(verify=False) as client:
        response = client.get(url)
        data = response.json()
        result = list(item for x in data["securities"]["data"] if (item := row_to_item(x)))
        sql = "INSERT OR IGNORE INTO SecurityData VALUES " \
              "(:isin, :secid, :issuesize, :issuesizeplaced, DATE(:settledate), :couponpercent, "\
              ":couponvalue, DATE(:nextcoupon), :couponperiod, :accruedint, :facevalue, :facevalueonsettledate, "\
              "DATE(:matdate), DATE(:offerdate), :buybackprice, DATE(:buybackdate))"
        with closing(connection.cursor()) as cursor:
            cursor.execute("DELETE FROM SecurityData")
            cursor.executemany(sql, [x.model_dump() for x in result])
            connection.commit()
        return result


def fetch_marketdata() -> Sequence[Union[SecurityMarketDataItem, None]]:
    columns = SecurityMarketDataItem.model_fields.keys()
    columns_query_value = ",".join(x.strip('_').upper() for x in columns)
    url = "https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?" \
          "iss.meta=off&iss.only=marketdata&"\
          f"marketdata.columns={columns_query_value}"

    def row_to_item(row):
        try:
            return SecurityMarketDataItem(**dict(zip(columns, row)))
        except ValidationError:
            return None

    with httpx.Client(verify=False) as client:
        response = client.get(url)
        data = response.json()
        return (item for x in data["marketdata"]["data"] if (item := row_to_item(x)))


def search_all(query: str = None) -> List[Union[SecuritySearchItem, None]]:
    columns = list(SecuritySearchItem.model_fields.keys())

    def row_to_item(row):
        try:
            return SecuritySearchItem(**dict(zip(columns, row)))
        except ValidationError:
            return None

    result = []
    limit = 100
    start = 0
    while True:
        part = search(query=query, start=start, limit=limit, columns=columns)
        result.extend(item for x in part if (item := row_to_item(x)))
        if len(part) < limit:
            break
        start = start + limit
    return result


def search(**kwargs):
    with httpx.Client(verify=False) as client:
        url = make_search_url(**kwargs)
        response = client.get(url)
        data = response.json()
        return data["securities"]["data"]


def make_search_url(query: str = None, start=0, limit=100, columns: List = None):
    columns_query_value = ",".join(columns)
    url = f"https://iss.moex.com/iss/securities.json?iss.meta=off&engine=stock&market=bonds" \
        f"&securities.columns={columns_query_value}" \
        f"&is_trading=1" \
        f"{('&q=' + query) if query else ''}" \
        f"&start={start}&limit={limit}"
    return url
