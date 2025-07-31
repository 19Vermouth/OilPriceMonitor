from dotenv import load_dotenv
import os

load_dotenv()
print("Alpha Vantage Key:", os.getenv("ALPHAVANTAGE_API_KEY"))
print("NewsAPI Key:", os.getenv("NEWSAPI_API_KEY"))
print("GNews Key:", os.getenv("GNEWS_API_KEY"))