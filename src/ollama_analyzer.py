import ollama
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class OilPriceChangeAnalyzer:
    def __init__(self, model_name: str = "mistral"):
        self.model_name = model_name
        
    def analyze_price_change(self, news_articles: List[Dict]) -> Dict:
        """Analyze news articles for price change reasons"""
        if not news_articles:
            return {"reasons": ["No relevant news articles found"]}
        
        context = "\n".join(
            f"Source: {art['source']['name']}\n"
            f"Title: {art['title']}\n"
            f"Description: {art['description']}\n"
            for art in news_articles
        )
        
        prompt = f"""
        Analyze these news articles about oil price changes and identify 
        factual reasons for recent price movements. Focus on:
        - Supply/demand changes
        - Geopolitical events
        - Economic factors
        - Weather/natural disasters
        
        News Context:
        {context}
        
        Provide concise bullet points:
        - [Reason 1]
        - [Reason 2]
        - [Reason 3]
        """
        
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={'temperature': 0.2}
            )
            return self._parse_response(response['response'])
        except Exception as e:
            logger.error(f"Ollama analysis failed: {e}")
            return {"error": str(e)}
    
    def _parse_response(self, response: str) -> Dict:
        reasons = []
        for line in response.split('\n'):
            if line.strip().startswith('- '):
                reasons.append(line[2:].strip())
        return {
            "reasons": reasons if reasons else ["No specific reasons identified"],
            "raw_response": response
        }