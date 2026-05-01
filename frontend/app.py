import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os
import sys

# Add backend to path to import agents for offline simulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.agents.agent_manager import AI_Agents

st.set_page_config(page_title="SentientBrand AI", layout="wide", page_icon="🧠")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    h1, h2, h3 { color: #00F0FF; font-family: 'Inter', sans-serif; }
    .stButton>button { border-radius: 20px; background-color: #00F0FF; color: black; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #00B8FF; }
    div[data-testid="stMetricValue"] { color: #00F0FF; }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 SentientBrand AI Intelligence Platform")
st.markdown("### Real-time Multi-Agent Social Media Analytics")

# Load model for offline use
MODEL_DIR = "backend/ml_model"
@st.cache_resource
def load_model():
    if os.path.exists(f"{MODEL_DIR}/sentiment_model.pkl"):
        model = joblib.load(f"{MODEL_DIR}/sentiment_model.pkl")
        vectorizer = joblib.load(f"{MODEL_DIR}/vectorizer.pkl")
        return model, vectorizer
    return None, None

model, vectorizer = load_model()

tabs = st.tabs(["📊 Live Intelligence Dashboard", "🤖 AI Copilot", "🗂️ Batch Analytics"])

with tabs[0]:
    st.header("Real-Time Sentiment Monitoring")
    if not model:
        st.warning("⚠️ Model not trained yet. Please run the training script first.")
    else:
        st.markdown("*(Simulating real-time data ingest...)*")
        # In a real app, we'd use WebSocket. Here we simulate for Streamlit offline stability.
        df = pd.read_csv("outputs/synthetic_social_data.csv") if os.path.exists("outputs/synthetic_social_data.csv") else pd.DataFrame()
        
        if not df.empty:
            df_recent = df.tail(100).copy()
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            pos_pct = len(df_recent[df_recent['sentiment'] == 'positive']) / len(df_recent) * 100
            neg_pct = len(df_recent[df_recent['sentiment'] == 'negative']) / len(df_recent) * 100
            
            col1.metric("Total Active Streams", f"{len(df_recent)}/hr")
            col2.metric("Positive Sentiment", f"{pos_pct:.1f}%")
            col3.metric("Negative Sentiment", f"{neg_pct:.1f}%", delta=f"{neg_pct - 15:.1f}% vs yesterday", delta_color="inverse")
            
            st.divider()
            
            # Agents Area
            st.subheader("🛡️ AI Agent Interventions")
            c1, c2 = st.columns(2)
            with c1:
                st.info("**Monitoring Agent Status:** Active")
                alerts = AI_Agents.monitoring_agent(df_recent.to_dict('records'))
                if alerts:
                    for alert in alerts:
                        st.error(alert)
                else:
                    st.success("✅ Systems Normal. No critical PR threats detected.")
            with c2:
                st.info("**Decision Agent Recommendation:**")
                st.write(AI_Agents.decision_agent(df_recent.to_dict('records')))
            
            # Charts
            fig = px.histogram(df_recent, x="sentiment", color="sentiment", 
                               color_discrete_map={"positive": "#00FF00", "negative": "#FF0000", "neutral": "#888888"},
                               title="Recent Sentiment Distribution")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.header("💬 AI Copilot")
    st.markdown("Ask the Copilot for deep insights or strategic recommendations based on current data.")
    
    query = st.text_input("Message Copilot:", placeholder="e.g., Why is negative sentiment high today?")
    if st.button("Ask"):
        if 'df_recent' in locals() and not df_recent.empty:
            stats = {
                'total': len(df_recent),
                'positive': len(df_recent[df_recent['sentiment'] == 'positive']),
                'negative': len(df_recent[df_recent['sentiment'] == 'negative'])
            }
            response = AI_Agents.copilot_agent(query, stats)
            st.success(f"🤖 **Copilot:** {response}")
        else:
            st.error("No data available to analyze.")

with tabs[2]:
    st.header("🗂️ Batch CSV Analyzer")
    file = st.file_uploader("Upload CSV file with a 'text' column")
    if file:
        df_upload = pd.read_csv(file)
        if 'text' in df_upload.columns and model:
            vec = vectorizer.transform(df_upload['text'].str.lower())
            df_upload['predicted_sentiment'] = model.predict(vec)
            st.dataframe(df_upload)
            
            fig = px.pie(df_upload, names='predicted_sentiment', title='Predicted Sentiment Breakdown')
            st.plotly_chart(fig)
        else:
            st.error("Invalid file or model not loaded.")
