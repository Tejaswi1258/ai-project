import re

class EmotionAnalyzer:
    def __init__(self):
        self.negations = ['not', "don't", "doesnt", "didn't", "never", "no", "can't",
                          "cannot", "won't", "isn't", "aren't", "dont", "wont", "isnt", "arent"]

        self.intensifiers = ['very', 'really', 'so', 'extremely', 'absolutely', 'totally',
                             'deeply', 'incredibly', 'terribly', 'quite', 'super', 'too']

        # implicit negative phrases that don't contain obvious sad/angry words
        self.implicit_sad = [
            "i'm not ok", "im not ok", "i am not ok", "not okay", "i'm not okay", "im not okay",
            "not doing well", "not doing good", "not feeling well", "not feeling good",
            "i give up", "i quit", "i can't do this", "i cant do this", "i can't anymore",
            "i cant anymore", "i don't want to", "i dont want to", "i don't care anymore",
            "i dont care anymore", "what's the point", "whats the point", "no point",
            "tired of everything", "tired of life", "tired of living", "done with everything",
            "done with life", "i'm done", "im done", "i am done", "nothing is fine",
            "everything is wrong", "i feel nothing", "feel nothing", "i feel empty",
            "i'm broken", "im broken", "i am broken", "i'm lost", "im lost",
            "i'm not fine", "im not fine", "i am not fine"
        ]

        self.crisis_phrases = [
            "want to die", "want to kill myself", "kill myself", "end my life", "end it all",
            "take my life", "suicide", "suicidal", "no reason to live", "don't want to live",
            "dont want to live", "rather be dead", "better off dead", "wish i was dead",
            "wish i were dead", "want to disappear", "want to vanish", "life is not worth",
            "life isnt worth", "can't go on", "cant go on", "i want to hurt myself",
            "hurt myself", "self harm", "cutting myself", "i want to end it"
        ]

        self.emotion_keywords = {
            'Happy': {
                'words': ['happy', 'joy', 'joyful', 'great', 'wonderful', 'amazing', 'love', 'fantastic',
                          'good', 'awesome', 'glad', 'pleased', 'delighted', 'cheerful', 'smile', 'laugh',
                          'blessed', 'grateful', 'thankful', 'enjoy', 'fun', 'excellent', 'brilliant',
                          'content', 'satisfied', 'proud', 'peaceful', 'relieved', 'optimistic', 'positive'],
                'phrases': ['feeling good', 'so happy', 'made my day', 'love it', 'best day',
                            'on top of the world', 'over the moon', 'feeling great', 'life is good',
                            'cant stop smiling', 'i am happy', 'i feel happy', 'i feel great']
            },
            'Sad': {
                'words': ['sad', 'unhappy', 'cry', 'crying', 'tears', 'depressed', 'depression', 'miserable',
                          'heartbroken', 'grief', 'sorrow', 'sorrowful', 'upset', 'gloomy', 'hopeless',
                          'hurt', 'pain', 'broken', 'empty', 'numb', 'regret', 'disappointed', 'failure',
                          'worthless', 'helpless', 'suffering', 'mourn', 'mourning', 'devastated', 'shattered',
                          'down', 'low', 'dull', 'tired', 'exhausted', 'drained', 'weak', 'lost'],
                'phrases': ['feel like crying', 'want to cry', 'breaking my heart', 'lost everything',
                            'feel so low', 'nothing matters', 'all alone', 'no one cares',
                            'feeling down', 'hit rock bottom', 'falling apart', 'i feel sad',
                            'i am sad', 'i feel bad', 'i feel terrible', 'i feel awful',
                            'i feel horrible', 'i feel lost', 'i feel empty', 'i feel broken',
                            'i feel hopeless', 'i feel worthless', 'i feel like nothing',
                            'i feel like a failure', 'i feel like giving up']
            },
            'Angry': {
                'words': ['angry', 'anger', 'furious', 'rage', 'hate', 'mad', 'annoyed', 'frustrated',
                          'irritated', 'outraged', 'bitter', 'hostile', 'aggressive', 'enraged',
                          'livid', 'infuriated', 'resentful', 'offended', 'despise', 'loathe', 'fuming'],
                'phrases': ['so angry', 'makes me mad', 'drives me crazy', 'fed up with', 'sick and tired',
                            'lost my temper', 'how dare', 'this is wrong', 'not fair', 'i am angry',
                            'i feel angry', 'i hate this', 'i hate everything', 'i hate my life']
            },
            'Anxious': {
                'words': ['anxious', 'anxiety', 'worried', 'nervous', 'scared', 'fear', 'afraid', 'panic',
                          'stress', 'stressed', 'tense', 'uneasy', 'dread', 'terror', 'frightened', 'insecure',
                          'overwhelmed', 'uncertain', 'doubt', 'confused', 'paranoid', 'restless',
                          'shaking', 'trembling', 'overthinking', 'dreading'],
                'phrases': ['what if', 'cant breathe', 'heart racing', 'freaking out', 'losing my mind',
                            'so stressed', 'cant sleep', 'keep thinking', 'worst case', 'something bad',
                            'i feel anxious', 'i am anxious', 'i feel nervous', 'i am nervous',
                            'i feel scared', 'i am scared', 'i feel worried', 'i am worried']
            },
            'Excited': {
                'words': ['excited', 'thrilled', 'ecstatic', 'eager', 'enthusiastic', 'pumped', 'hyped',
                          'incredible', 'astonished', 'amazed', 'energetic', 'motivated', 'inspired',
                          'elated', 'overjoyed', 'stoked', 'psyched', 'fired up', 'buzzing', 'yay'],
                'phrases': ['cant wait', 'looking forward', 'so excited', 'best news', 'this is amazing',
                            'oh my god', 'finally happened', 'dream come true', 'i am excited',
                            'i feel excited', 'i am thrilled', 'i feel thrilled']
            },
            'Lonely': {
                'words': ['lonely', 'alone', 'isolated', 'abandoned', 'forgotten', 'invisible', 'disconnected',
                          'excluded', 'unwanted', 'unloved', 'ignored', 'rejected', 'friendless', 'outsider'],
                'phrases': ['no one understands', 'no one cares', 'all by myself', 'feel invisible',
                            'no friends', 'nobody talks to me', 'left behind', 'on my own',
                            'no one to talk to', 'feel so alone', 'nobody loves me',
                            'i feel lonely', 'i am lonely', 'i feel alone', 'i am alone',
                            'i feel isolated', 'no one is there', 'nobody is there']
            },
            'Disgusted': {
                'words': ['disgusted', 'disgust', 'gross', 'revolting', 'nasty', 'repulsed', 'appalled',
                          'horrified', 'dreadful', 'vile', 'filthy', 'repulsive', 'nauseating', 'pathetic'],
                'phrases': ['makes me sick', 'so disgusting', 'how could they', 'this is horrible',
                            'absolutely awful', 'i feel disgusted', 'i am disgusted']
            },
            'Surprised': {
                'words': ['surprised', 'shocked', 'unexpected', 'astonished', 'stunned', 'speechless', 'omg'],
                'phrases': ['did not expect', 'out of nowhere', 'never saw it coming', 'caught off guard',
                            'blew my mind', 'cant believe it', 'totally unexpected', 'i am shocked',
                            'i feel shocked', 'i am surprised']
            },
            'Hopeless': {
                'words': ['hopeless', 'worthless', 'useless', 'pointless', 'meaningless', 'purposeless',
                          'doomed', 'trapped', 'stuck', 'suffocating', 'drowning', 'sinking'],
                'phrases': ['no hope', 'no future', 'no way out', 'nothing will change', 'nothing gets better',
                            'i feel hopeless', 'i am hopeless', 'i feel worthless', 'i am worthless',
                            'i feel useless', 'i am useless', 'i see no point', 'there is no point',
                            'i feel trapped', 'i feel stuck', 'i feel like giving up', 'i give up']
            }
        }

    def _contains_negation(self, words, idx):
        start = max(0, idx - 3)
        return any(w in self.negations for w in words[start:idx])

    def _get_intensifier_boost(self, words, idx):
        start = max(0, idx - 2)
        return 1.5 if any(w in self.intensifiers for w in words[start:idx]) else 1.0

    def analyze(self, text):
        text_lower = text.lower().strip()
        text_lower = re.sub(r"['\u2019]", "'", text_lower)
        words = re.findall(r"\b\w+\b", text_lower)
        scores = {emotion: 0.0 for emotion in self.emotion_keywords}

        # crisis detection - highest priority
        for phrase in self.crisis_phrases:
            if phrase in text_lower:
                return {
                    "emotion": "Hopeless",
                    "confidence": 99.0,
                    "original_label": "hopeless",
                    "alert": "⚠️ Please reach out to a mental health professional or call a helpline immediately."
                }

        # implicit sad phrase detection
        for phrase in self.implicit_sad:
            if phrase in text_lower:
                scores['Sad'] += 3.0

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
                        # negated positive = sad
                        if emotion == 'Happy':
                            scores['Sad'] += 1.5
                        else:
                            scores[emotion] -= 0.5
                    else:
                        boost = self._get_intensifier_boost(words, idx)
                        scores[emotion] += boost

        top_emotion = max(scores, key=scores.get)
        top_score = scores[top_emotion]

        if top_score <= 0:
            # fallback: short negative statements
            negative_words = ['bad', 'wrong', 'terrible', 'horrible', 'awful', 'worst', 'hate',
                               'sick', 'tired', 'bored', 'dull', 'meh', 'ugh', 'ew', 'blah']
            if any(w in words for w in negative_words):
                return {"emotion": "Sad", "confidence": 72.0, "original_label": "sad"}
            return {"emotion": "Neutral", "confidence": 85.0, "original_label": "neutral"}

        positive_scores = {e: s for e, s in scores.items() if s > 0}
        total = sum(positive_scores.values())
        confidence = round((top_score / total) * 100, 2)
        confidence = max(min(confidence, 99.0), 55.0)

        return {
            "emotion": top_emotion,
            "confidence": confidence,
            "original_label": top_emotion.lower()
        }
