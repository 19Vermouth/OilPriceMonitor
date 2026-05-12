from geip.schemas import Region, RiskScore
from fastapi import APIRouter

router = APIRouter()

REGIONAL_RISKS = {
    "MIDDLE_EAST": 78.0,
    "NORTH_AMERICA": 35.0,
    "EUROPE": 42.0,
    "ASIA_PACIFIC": 55.0,
    "AFRICA": 68.0,
    "LATIN_AMERICA": 52.0,
}

COUNTRY_RISKS = {
    "SA": {"name": "Saudi Arabia", "risk": 82, "lat": 23.8859, "lon": 45.0792},
    "IR": {"name": "Iran", "risk": 85, "lat": 32.4279, "lon": 53.6880},
    "IQ": {"name": "Iraq", "risk": 75, "lat": 33.3152, "lon": 44.3661},
    "AE": {"name": "UAE", "risk": 35, "lat": 23.4241, "lon": 53.8478},
    "KW": {"name": "Kuwait", "risk": 40, "lat": 29.3117, "lon": 47.4818},
    "US": {"name": "United States", "risk": 25, "lat": 37.0902, "lon": -95.7129},
    "RU": {"name": "Russia", "risk": 65, "lat": 61.5240, "lon": 105.3188},
    "CN": {"name": "China", "risk": 45, "lat": 35.8617, "lon": 104.1954},
    "IN": {"name": "India", "risk": 50, "lat": 20.5937, "lon": 78.9629},
    "NG": {"name": "Nigeria", "risk": 72, "lat": 9.0820, "lon": 8.6753},
    "VE": {"name": "Venezuela", "risk": 80, "lat": 6.4238, "lon": -66.5897},
    "LY": {"name": "Libya", "risk": 78, "lat": 26.3351, "lon": 17.2283},
    "SD": {"name": "Sudan", "risk": 70, "lat": 12.8628, "lon": 30.2176},
    "YE": {"name": "Yemen", "risk": 88, "lat": 15.5527, "lon": 48.5164},
    "UA": {"name": "Ukraine", "risk": 75, "lat": 48.3794, "lon": 31.1656},
    "GB": {"name": "United Kingdom", "risk": 30, "lat": 55.3781, "lon": -3.4360},
    "DE": {"name": "Germany", "risk": 28, "lat": 51.1657, "lon": 10.4515},
    "FR": {"name": "France", "risk": 25, "lat": 46.2276, "lon": 2.2137},
    "BR": {"name": "Brazil", "risk": 48, "lat": -14.2350, "lon": -51.9253},
    "ID": {"name": "Indonesia", "risk": 42, "lat": -0.7893, "lon": 113.9213},
}


@router.get("/global")
async def global_risk():
    return {
        "region": None,
        "global_score": 62.5,
        "level": "Moderate",
        "factors": ["Middle East tensions", "OPEC+ policy uncertainty", "US inventory data"]
    }


@router.get("/region/{region}")
async def regional_risk(region: Region):
    score = REGIONAL_RISKS.get(region.value, 50.0)
    return {
        "region": region.value,
        "global_score": score,
        "level": "Moderate" if score < 70 else "High",
        "factors": ["Regional supply dynamics", "Policy changes"]
    }


@router.get("/heatmap")
async def risk_heatmap():
    return {
        "countries": [
            {"code": code, "name": data["name"], "risk": data["risk"], "lat": data["lat"], "lon": data["lon"]}
            for code, data in COUNTRY_RISKS.items()
        ],
        "regions": REGIONAL_RISKS,
    }
