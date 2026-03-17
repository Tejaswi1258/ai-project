import re

class EmotionAnalyzer:
    def __init__(self):
        self.negations = ['not', "don't", "doesn't", "didn't", "never", "no", "can't", "cannot", "won't", "isn't", "aren't"]

        self.intensifiers = ['very', 'really', 'so', 'extremely', 'absolutely', 'totally', 'deeply', 'incredibly', 'terribly', 'quite']

        self.emotion_keywords = {
            'Happy': {
                'words': ['happy', 'joy', 'joyful', 'great', 'wonderful', 'amazing', 'love', 'fantastic',
                          'good', 'awesome', 'glad', 'pleased', 'delighted', 'cheerful', 'smile', 'laugh',
                          'blessed', 'grateful', 'thankful', 'enjoy', 'fun', 'excellent', 'brilliant',
                          'content', 'satisfied', 'proud', 'peaceful', 'relieved', 'optimistic', 'positive'],
                'phrases': ['feeling good', 'so happy', 'made my day', 'love it', 'best day', 'on top of the world',
                            'over the moon', 'feeling great', 'life is good', 'cant stop smiling']
            },
            'Sad': {
                'words': ['sad', 'unhappy', 'cry', 'crying', 'tears', 'depressed', 'depression', 'miserable',
                          'heartbroken', 'grief', 'sorrow', 'sorrowful', 'upset', 'gloomy', 'hopeless',
                          'hurt', 'pain', 'broken', 'empty', 'numb', 'regret', 'disappointed', 'failure',
                          'worthless', 'helpless', 'suffering', 'mourn', 'mourning', 'devastated', 'shattered'],
                'phrases': ['feel like crying', 'want to cry', 'breaking my heart', 'lost everything',
                            'no reason to live', 'feel so low', 'nothing matters', 'all alone', 'no one cares',
                            'feeling down', 'hit rock bottom', 'falling apart']
            },
            'Angry': {
                'words': ['angry', 'anger', 'furious', 'rage', 'hate', 'mad', 'annoyed', 'frustrated',
                          'irritated', 'outraged', 'disgusted', 'bitter', 'hostile', 'aggressive',
                          'enraged', 'livid', 'infuriated', 'resentful', 'offended', 'fed up',
                          'sick of', 'cant stand', 'despise', 'loathe', 'boiling', 'fuming'],
                'phrases': ['so angry', 'makes me mad', 'drives me crazy', 'fed up with', 'sick and tired',
                            'lost my temper', 'how dare', 'this is wrong', 'not fair', 'pisses me off']
            },
            'Anxious': {
                'words': ['anxious', 'anxiety', 'worried', 'nervous', 'scared', 'fear', 'afraid', 'panic',
                          'stress', 'stressed', 'tense', 'uneasy', 'dread', 'terror', 'frightened', 'insecure',
                          'overwhelmed', 'uncertain', 'doubt', 'confused', 'trouble', 'paranoid',
                          'restless', 'shaking', 'trembling', 'sweating', 'overthinking', 'dreading'],
                'phrases': ['what if', 'cant breathe', 'heart racing', 'freaking out', 'losing my mind',
                            'so stressed', 'cant sleep', 'keep thinking', 'worst case', 'something bad']
            },
            'Excited': {
                'words': ['excited', 'thrilled', 'ecstatic', 'eager', 'enthusiastic', 'pumped', 'hyped',
                          'incredible', 'unbelievable', 'surprised', 'shocked', 'astonished', 'amazed',
                          'energetic', 'motivated', 'inspired', 'elated', 'overjoyed', 'stoked',
                          'psyched', 'fired up', 'buzzing', 'wow', 'woah', 'yay', 'whoa'],
                'phrases': ['cant wait', 'looking forward', 'so excited', 'best news', 'this is amazing',
                            'oh my god', 'no way', 'this is great', 'finally happened', 'dream come true']
            },
            'Lonely': {
                'words': ['lonely', 'alone', 'isolated', 'abandoned', 'forgotten', 'invisible', 'disconnected',
                          'excluded', 'unwanted', 'unloved', 'ignored', 'rejected', 'solitude', 'apart',
                          'missing', 'longing', 'yearning', 'nobody', 'friendless', 'left out', 'outsider'],
                'phrases': ['no one understands', 'no one cares', 'all by myself', 'feel invisible',
                            'no friends', 'nobody talks to me', 'left behind', 'on my own',
                            'no one to talk to', 'feel so alone', 'nobody loves me']
            },
            'Disgusted': {
                'words': ['disgusted', 'disgust', 'gross', 'revolting', 'nasty', 'sick', 'repulsed',
                          'appalled', 'horrified', 'awful', 'terrible', 'dreadful', 'vile', 'filthy',
                          'repulsive', 'nauseating', 'yuck', 'eww', 'pathetic', 'shameful'],
                'phrases': ['makes me sick', 'so disgusting', 'cant believe', 'how could they',
                            'this is horrible', 'absolutely awful', 'makes me want to vomit']
            },
            'Surprised': {
                'words': ['surprised', 'surprise', 'shocked', 'unexpected', 'sudden', 'unbelievable',
                          'astonished', 'stunned', 'speechless', 'disbelief', 'jaw drop', 'whoa',
                          'wow', 'really', 'seriously', 'no way', 'what', 'omg'],
                'phrases': ['did not expect', 'out of nowhere', 'came out of nowhere', 'never saw it coming',
                            'caught off guard', 'blew my mind', 'cant believe it', 'totally unexpected']
            }
        }

    def _contains_negation(self, words, idx):
        start = max(0, idx - 3)
        return any(w in self.negations for w in words[start:idx])

    def _get_intensifier_boost(self, words, idx):
        start = max(0, idx - 2)
        return 1.5 if any(w in self.intensifiers for w in words[start:idx]) else 1.0

    def analyze(self, text):
        text_lower = text.lower()
        words = re.findall(r"\b\w+\b", text_lower)
        scores = {emotion: 0.0 for emotion in self.emotion_keywords}

        # phrase matching
        for emotion, data in self.emotion_keywords.items():
            for phrase in data['phrases']:
                if phrase in text_lower:
                    scores[emotion] += 2.0

        # word matching with negation and intensifier
        for idx, word in enumerate(words):
            for emotion, data in self.emotion_keywords.items():
                if word in data['words']:
                    if self._contains_negation(words, idx):
                        scores[emotion] -= 1.0
                    else:
                        boost = self._get_intensifier_boost(words, idx)
                        scores[emotion] += boost

        top_emotion = max(scores, key=scores.get)
        top_score = scores[top_emotion]

        if top_score <= 0:
            return {"emotion": "Neutral", "confidence": 95.0, "original_label": "neutral"}

        positive_scores = {e: s for e, s in scores.items() if s > 0}
        total = sum(positive_scores.values())
        confidence = round((top_score / total) * 100, 2)
        confidence = max(min(confidence, 99.0), 40.0)

        return {
            "emotion": top_emotion,
            "confidence": confidence,
            "original_label": top_emotion.lower()
        }
