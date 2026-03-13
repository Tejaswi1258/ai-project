from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    def analyze(self, text):
        result = self.classifier(text)[0]
        return {
            "sentiment": result["label"],
            "confidence": round(result["score"] * 100, 2)
        }
