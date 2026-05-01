import random

class AI_Agents:
    """
    Simulates a Multi-Agent AI System to provide intelligent insights, alerts, and conversational capabilities.
    In a true production environment, this would integrate with LangChain / OpenAI / LLaMA.
    """
    
    @staticmethod
    def monitoring_agent(sentiment_data):
        """
        Monitors the real-time data stream and flags anomalies.
        """
        total = len(sentiment_data)
        if total == 0:
            return None
            
        negative_count = len([x for x in sentiment_data if x['sentiment'] == 'negative'])
        neg_ratio = negative_count / total
        
        alerts = []
        if neg_ratio > 0.4:
            alerts.append(f"🚨 CRITICAL: Negative sentiment spiked to {neg_ratio*100:.1f}%. Immediate PR intervention recommended.")
        elif neg_ratio > 0.2:
            alerts.append(f"⚠️ WARNING: Elevated negative sentiment detected ({neg_ratio*100:.1f}%).")
            
        return alerts

    @staticmethod
    def decision_agent(sentiment_data):
        """
        Analyzes the trend and recommends business decisions.
        """
        total = len(sentiment_data)
        if total == 0:
            return "No data to analyze."
            
        positive = len([x for x in sentiment_data if x['sentiment'] == 'positive'])
        negative = len([x for x in sentiment_data if x['sentiment'] == 'negative'])
        
        pos_ratio = positive / total
        neg_ratio = negative / total
        
        if pos_ratio > 0.6:
            return "💡 DECISION: Positive sentiment is high. Recommend launching up-sell campaigns or referral programs."
        elif neg_ratio > 0.3:
            return "🛡️ DECISION: High dissatisfaction. Recommend halting current marketing ads and deploying customer support teams."
        else:
            return "📊 DECISION: Sentiment is stable. Continue normal operations and monitor."

    @staticmethod
    def copilot_agent(user_query, current_stats):
        """
        A simulated AI assistant that answers questions based on current dashboard state.
        """
        query = user_query.lower()
        
        if "summary" in query or "status" in query:
            return f"Currently, we have {current_stats['total']} mentions. Positive: {current_stats['positive']}, Negative: {current_stats['negative']}."
        elif "why" in query and "negative" in query:
            return "Based on text clustering, negative comments are primarily related to 'app crashing' and 'delivery delay'."
        elif "what should i do" in query or "recommendation" in query:
            return AI_Agents.decision_agent([{'sentiment': 'positive'}] * current_stats['positive'] + [{'sentiment': 'negative'}] * current_stats['negative'])
        else:
            return "I am the SentientBrand Copilot. Ask me for a summary, why sentiment is negative, or for strategic recommendations!"
