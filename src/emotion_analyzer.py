from transformers import pipeline

class EmotionAnalyzer:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
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
        result = self.classifier(text)[0]
        emotion = result['label']
        mapped_emotion = self.emotion_map.get(emotion, emotion)
        
        return {
            "emotion": mapped_emotion,
            "confidence": round(result["score"] * 100, 2),
            "original_label": emotion
        }
