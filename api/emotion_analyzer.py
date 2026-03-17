import urllib.request
import json
import os

class EmotionAnalyzer:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
        self.api_token = os.environ.get("HF_API_TOKEN", "")
        self.emotion_map = {
            'joy': 'Happy',
            'sadness': 'Sad',
            'anger': 'Angry',
            'fear': 'Anxious',
            'surprise': 'Excited',
            'disgust': 'Disgusted',
            'neutral': 'Neutral'
        }

    def analyze(self, text):
        payload = json.dumps({"inputs": text}).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        req = urllib.request.Request(self.api_url, data=payload, headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())[0]

        top = max(result, key=lambda x: x['score'])
        return {
            "emotion": self.emotion_map.get(top['label'], top['label']),
            "confidence": round(top['score'] * 100, 2),
            "original_label": top['label']
        }
