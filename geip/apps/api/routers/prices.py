import random
from fastapi import APIRouter
from geip.schemas import CrudeType, PriceData

router = APIRouter()

BARREL_TO_LITER = 158.987
USD_TO_LOCAL = {
    "US": 1.0, "DE": 0.92, "GB": 0.79, "FR": 0.92, "IT": 0.92,
    "JP": 149.5, "CN": 7.25, "IN": 83.1, "BR": 4.97, "CA": 1.36,
    "AU": 1.53, "MX": 17.15, "KR": 1320, "SA": 3.75, "RU": 92.5,
    "ID": 15600, "TR": 32.1, "ZA": 18.9, "AR": 870, "TH": 35.5,
}

BASE_OIL_PRICE_USD = 78.50

TOP_20_CONSUMPTION = [
    {"country": "United States", "code": "US", "consumption_mbd": 20.0, "consumption_twh": 4000},
    {"country": "China", "code": "CN", "consumption_mbd": 16.0, "consumption_twh": 7500},
    {"country": "India", "code": "IN", "consumption_mbd": 5.5, "consumption_twh": 1800},
    {"country": "Russia", "code": "RU", "consumption_mbd": 3.7, "consumption_twh": 1100},
    {"country": "Japan", "code": "JP", "consumption_mbd": 3.5, "consumption_twh": 950},
    {"country": "Saudi Arabia", "code": "SA", "consumption_mbd": 3.4, "consumption_twh": 450},
    {"country": "Brazil", "code": "BR", "consumption_mbd": 3.0, "consumption_twh": 1200},
    {"country": "South Korea", "code": "KR", "consumption_mbd": 2.8, "consumption_twh": 650},
    {"country": "Germany", "code": "DE", "consumption_mbd": 2.4, "consumption_twh": 900},
    {"country": "Canada", "code": "CA", "consumption_mbd": 2.3, "consumption_twh": 850},
    {"country": "Mexico", "code": "MX", "consumption_mbd": 2.0, "consumption_twh": 600},
    {"country": "Indonesia", "code": "ID", "consumption_mbd": 1.8, "consumption_twh": 550},
    {"country": "France", "code": "FR", "consumption_mbd": 1.6, "consumption_twh": 700},
    {"country": "United Kingdom", "code": "GB", "consumption_mbd": 1.5, "consumption_twh": 650},
    {"country": "Italy", "code": "IT", "consumption_mbd": 1.3, "consumption_twh": 580},
    {"country": "Australia", "code": "AU", "consumption_mbd": 1.2, "consumption_twh": 480},
    {"country": "Turkey", "code": "TR", "consumption_mbd": 1.1, "consumption_twh": 420},
    {"country": "Thailand", "code": "TH", "consumption_mbd": 1.0, "consumption_twh": 380},
    {"country": "South Africa", "code": "ZA", "consumption_mbd": 0.9, "consumption_twh": 350},
    {"country": "Argentina", "code": "AR", "consumption_mbd": 0.8, "consumption_twh": 320},
]


def calculate_price_per_liter(country_code: str) -> dict:
    base_usd = BASE_OIL_PRICE_USD + random.uniform(-2, 2)
    price_per_barrel = base_usd
    price_per_liter_usd = price_per_barrel / BARREL_TO_LITER
    
    exchange_rate = USD_TO_LOCAL.get(country_code, 1.0)
    tax_multiplier = random.uniform(1.5, 3.0)
    price_per_liter_local = price_per_liter_usd * exchange_rate * tax_multiplier
    
    return {
        "per_barrel_usd": round(price_per_barrel, 2),
        "per_liter_usd": round(price_per_liter_usd, 4),
        "per_liter_local": round(price_per_liter_local, 2),
        "currency": get_currency(country_code),
    }


def get_currency(code: str) -> str:
    currencies = {
        "US": "USD", "DE": "EUR", "GB": "GBP", "FR": "EUR", "IT": "EUR",
        "JP": "JPY", "CN": "CNY", "IN": "INR", "BR": "BRL", "CA": "CAD",
        "AU": "AUD", "MX": "MXN", "KR": "KRW", "SA": "SAR", "RU": "RUB",
        "ID": "IDR", "TR": "TRY", "ZA": "ZAR", "AR": "ARS", "TH": "THB",
    }
    return currencies.get(code, "USD")


@router.get("/latest")
async def latest():
    return {
        "prices": [
            PriceData(
                crude_type=crude,
                price=price,
                timestamp=datetime.now(timezone.utc)
            )
            for crude, price in {
                CrudeType.WTI: 78.50,
                CrudeType.BRENT: 82.30,
                CrudeType.DUBAI: 80.15,
                CrudeType.OPEC_BASKET: 79.00,
            }.items()
        ]
    }


@router.get("/history")
async def history(crude_type: CrudeType = CrudeType.WTI, days: int = 30):
    return {"prices": []}


@router.get("/consumption")
async def get_consumption():
    data = []
    for item in TOP_20_CONSUMPTION:
        prices = calculate_price_per_liter(item["code"])
        data.append({
            "rank": len(data) + 1,
            "country": item["country"],
            "code": item["code"],
            "consumption_mbd": item["consumption_mbd"],
            "consumption_twh": item["consumption_twh"],
            "price_per_barrel_usd": prices["per_barrel_usd"],
            "price_per_liter_usd": prices["per_liter_usd"],
            "price_per_liter_local": prices["per_liter_local"],
            "currency": prices["currency"],
        })
    return {"data": data, "updated": datetime.now(timezone.utc).isoformat()}


from datetime import datetime, timezone
