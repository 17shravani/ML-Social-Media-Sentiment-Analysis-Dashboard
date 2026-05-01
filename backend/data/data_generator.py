import pandas as pd
import random
import os

def generate_synthetic_data(num_samples=1000, output_path="outputs/synthetic_social_data.csv"):
    """
    Generates synthetic social media comments to simulate real-world data streams.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    positive_phrases = [
        "Absolutely love this new feature!", "Great customer service.", 
        "The delivery was super fast, highly recommend.", "Best product I have ever bought.",
        "Incredible experience, will buy again.", "So happy with the quality.",
        "They really outdid themselves this time.", "5 stars! Excellent work.",
        "The AI recommendations are spot on.", "Fantastic UI update."
    ]
    
    negative_phrases = [
        "Terrible experience, my app keeps crashing.", "Worst customer support ever.",
        "Delivery was delayed by 3 days.", "Product arrived damaged.",
        "I hate the new update, it's so confusing.", "Overpriced and underdelivered.",
        "Completely useless feature.", "I want a refund right now.",
        "The AI is hallucinating and giving wrong info.", "Never buying from them again."
    ]
    
    neutral_phrases = [
        "Just received my package.", "The app has been updated.",
        "It works okay, nothing special.", "Average experience.",
        "I guess it's fine for the price.", "It does what it says.",
        "No strong feelings about this.", "Standard delivery time.",
        "UI is different, still getting used to it.", "Let's see how long this lasts."
    ]
    
    data = []
    for _ in range(num_samples):
        sentiment = random.choice(["positive", "negative", "neutral"])
        if sentiment == "positive":
            text = random.choice(positive_phrases) + " " + random.choice(["😊", "👍", "", "!!"])
        elif sentiment == "negative":
            text = random.choice(negative_phrases) + " " + random.choice(["😡", "👎", "", "!?"])
        else:
            text = random.choice(neutral_phrases) + " " + random.choice(["😐", "", "."])
            
        # Add some noise/randomness
        if random.random() > 0.8:
            text = text.lower()
            
        data.append({
            "timestamp": pd.Timestamp.now() - pd.Timedelta(minutes=random.randint(0, 10000)),
            "platform": random.choice(["Twitter", "YouTube", "Reddit", "AppStore"]),
            "text": text.strip(),
            "sentiment": sentiment
        })
        
    df = pd.DataFrame(data)
    df.sort_values("timestamp", inplace=True)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Success: Generated {num_samples} synthetic records at {output_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_data(2000)
