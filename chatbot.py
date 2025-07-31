import streamlit as st
from streamlit_chat import message
from src.ollama_analyzer import OilPriceChangeAnalyzer
from src.news_aggregator import NewsAggregator
import time

# Initialize components with caching
@st.cache_resource
def get_components():
    return {
        "analyzer": OilPriceChangeAnalyzer(),
        "news_agg": NewsAggregator()
    }

def generate_response(user_input):
    """Generate AI response based on user query"""
    components = get_components()
    
    if "oil price" in user_input.lower():
        with st.spinner("🔍 Analyzing market conditions..."):
            articles = components["news_agg"].fetch_price_change_reasons()
            analysis = components["analyzer"].analyze_price_change(articles or [])
            
            if 'reasons' in analysis:
                response = "Current oil price drivers:\n" + "\n".join(f"- {r}" for r in analysis['reasons'])
            else:
                response = "Couldn't determine recent price changes. Try asking more specifically."
    else:
        response = f"I can help analyze oil prices. You asked: '{user_input}'"
    
    return response

def main():
    st.title("🛢️ Oil Market Chatbot")
    st.markdown("Ask about crude oil price trends and market drivers")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you with oil market analysis today?"}
        ]

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            message(msg["content"], is_user=True, key=f"user_{time.time()}")
        else:
            message(msg["content"], key=f"assistant_{time.time()}")

    # Chat input
    if prompt := st.chat_input("Ask about oil prices..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate response
        response = generate_response(prompt)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to show new messages
        st.rerun()

if __name__ == "__main__":
    main()