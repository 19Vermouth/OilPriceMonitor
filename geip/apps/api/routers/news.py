from fastapi import APIRouter

from geip.ingestion import cache, get_energy_news
from geip.pipeline import bronze

router = APIRouter()


@router.get("/news")
async def news(limit: int = 10):
    cache_key = f"news:energy:{limit}"
    cached = cache.get(cache_key)
    if cached:
        return {"articles": cached, "cached": True}
    
    articles = get_energy_news(limit=limit)
    cache.set(cache_key, articles, ttl=600)
    
    try:
        bronze.ingest_news(articles)
    except Exception:
        pass
    
    return {"articles": articles, "cached": False}
