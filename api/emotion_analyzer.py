class EmotionAnalyzer:
    def __init__(self):
        self.emotion_keywords = {
            'Happy': ['happy', 'joy', 'great', 'wonderful', 'amazing', 'love', 'excited', 'fantastic',
                      'good', 'awesome', 'glad', 'pleased', 'delighted', 'cheerful', 'smile', 'laugh',
                      'blessed', 'grateful', 'thankful', 'enjoy', 'fun', 'best', 'excellent', 'brilliant'],
            'Sad': ['sad', 'unhappy', 'cry', 'tears', 'depressed', 'miserable', 'heartbroken', 'grief',
                    'sorrow', 'upset', 'down', 'gloomy', 'hopeless', 'lonely', 'alone', 'miss', 'lost',
                    'hurt', 'pain', 'broken', 'empty', 'numb', 'regret', 'disappointed', 'failure'],
            'Angry': ['angry', 'anger', 'furious', 'rage', 'hate', 'mad', 'annoyed', 'frustrated',
                      'irritated', 'outraged', 'disgusted', 'bitter', 'hostile', 'violent', 'aggressive',
                      'enraged', 'livid', 'infuriated', 'resentful', 'offended', 'terrible', 'awful'],
            'Anxious': ['anxious', 'anxiety', 'worried', 'nervous', 'scared', 'fear', 'afraid', 'panic',
                        'stress', 'stressed', 'tense', 'uneasy', 'dread', 'terror', 'frightened', 'insecure',
                        'overwhelmed', 'helpless', 'uncertain', 'doubt', 'confused', 'lost', 'trouble'],
            'Excited': ['excited', 'thrilled', 'ecstatic', 'eager', 'enthusiastic', 'pumped', 'hyped',
                        'wow', 'incredible', 'unbelievable', 'surprised', 'shocked', 'astonished', 'amazed',
                        'cant wait', 'looking forward', 'anticipate', 'energetic', 'motivated', 'inspired'],
            'Lonely': ['lonely', 'alone', 'isolated', 'abandoned', 'forgotten', 'invisible', 'nobody',
                       'no one', 'empty', 'missing', 'longing', 'yearning', 'disconnected', 'excluded',
                       'left out', 'unwanted', 'unloved', 'ignored', 'rejected', 'solitude', 'apart']
        }

    def analyze(self, text):
        text_lower = text.lower()
        scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for word in keywords if word in text_lower)
            scores[emotion] = score

        top_emotion = max(scores, key=scores.get)
        top_score = scores[top_emotion]

        if top_score == 0:
            return {"emotion": "Neutral", "confidence": 95.0, "original_label": "neutral"}

        total = sum(scores.values())
        confidence = round((top_score / total) * 100, 2)

        return {
            "emotion": top_emotion,
            "confidence": confidence,
            "original_label": top_emotion.lower()
        }
