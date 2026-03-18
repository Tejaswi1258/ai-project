import re

class EmotionAnalyzer:
    def __init__(self):
        self.negations = ['not', "don't", "doesnt", "didn't", "never", "no", "can't",
                          "cannot", "won't", "isn't", "aren't", "dont", "wont", "isnt", "arent"]

        self.intensifiers = {
            'high': ['extremely', 'absolutely', 'completely', 'totally', 'deeply', 'incredibly',
                     'terribly', 'so much', 'beyond', 'utterly', 'desperately', 'severely'],
            'medium': ['very', 'really', 'quite', 'pretty', 'fairly', 'rather', 'super', 'too'],
            'low': ['a bit', 'slightly', 'kind of', 'kinda', 'somewhat', 'a little', 'sort of']
        }

        self.sarcasm_patterns = [
            r'oh great', r'oh wonderful', r'oh fantastic', r'yeah right', r'sure sure',
            r'totally fine', r'absolutely fine', r'oh perfect', r'just perfect',
            r'wow amazing', r'oh how lovely', r'oh how nice', r'oh how wonderful'
        ]

        self.crisis_phrases = [
            "want to die", "want to kill myself", "kill myself", "end my life", "end it all",
            "take my life", "suicide", "suicidal", "no reason to live", "don't want to live",
            "dont want to live", "rather be dead", "better off dead", "wish i was dead",
            "wish i were dead", "want to disappear", "life is not worth", "cant go on",
            "i want to hurt myself", "hurt myself", "self harm", "want to end it"
        ]

        self.violence_phrases = [
            "want to kill", "want to hurt", "going to kill", "gonna kill", "i will kill",
            "i want to kill", "kill him", "kill her", "kill them", "kill everyone",
            "kill my", "murder", "want to murder", "going to murder", "gonna murder",
            "i will murder", "beat him up", "beat her up", "beat them up", "destroy him",
            "destroy her", "destroy them", "make them suffer", "make him suffer",
            "make her suffer", "hurt him", "hurt her", "hurt them", "attack him",
            "attack her", "attack them", "stab", "shoot him", "shoot her", "shoot them",
            "i hate him so much i want to", "i hate her so much i want to",
            "want to harm", "going to harm", "planning to hurt", "planning to kill"
        ]

        self.implicit_sad = [
            "i'm not ok", "im not ok", "i am not ok", "not okay", "i'm not okay",
            "not doing well", "not doing good", "not feeling well", "not feeling good",
            "i give up", "i cant do this", "i can't anymore", "i cant anymore",
            "what's the point", "whats the point", "no point", "tired of everything",
            "tired of life", "done with everything", "i'm done", "im done",
            "nothing is fine", "everything is wrong", "i feel nothing", "i feel empty",
            "i'm broken", "im broken", "i'm lost", "im lost", "i'm not fine", "im not fine"
        ]

        self.emotion_keywords = {
            'Happy': {
                'words': ['happy', 'joy', 'joyful', 'great', 'wonderful', 'amazing', 'love', 'fantastic',
                          'good', 'awesome', 'glad', 'pleased', 'delighted', 'cheerful', 'smile', 'laugh',
                          'blessed', 'grateful', 'thankful', 'enjoy', 'fun', 'excellent', 'brilliant',
                          'content', 'satisfied', 'proud', 'peaceful', 'relieved', 'optimistic'],
                'phrases': ['feeling good', 'so happy', 'made my day', 'love it', 'best day',
                            'on top of the world', 'over the moon', 'feeling great', 'life is good',
                            'i am happy', 'i feel happy', 'i feel great', 'cant stop smiling']
            },
            'Excited': {
                'words': ['excited', 'thrilled', 'ecstatic', 'eager', 'enthusiastic', 'pumped', 'hyped',
                          'energetic', 'motivated', 'inspired', 'elated', 'overjoyed', 'stoked',
                          'psyched', 'fired up', 'buzzing', 'yay', 'woah', 'wow'],
                'phrases': ['cant wait', 'looking forward', 'so excited', 'best news', 'this is amazing',
                            'oh my god', 'finally happened', 'dream come true', 'i am excited']
            },
            'Sad': {
                'words': ['sad', 'unhappy', 'cry', 'crying', 'tears', 'depressed', 'depression', 'miserable',
                          'heartbroken', 'grief', 'sorrow', 'upset', 'gloomy', 'hopeless', 'hurt', 'pain',
                          'broken', 'empty', 'numb', 'regret', 'disappointed', 'failure', 'worthless',
                          'helpless', 'suffering', 'devastated', 'shattered', 'down', 'drained', 'lost'],
                'phrases': ['feel like crying', 'want to cry', 'breaking my heart', 'lost everything',
                            'feel so low', 'nothing matters', 'no one cares', 'feeling down',
                            'hit rock bottom', 'falling apart', 'i feel sad', 'i am sad',
                            'i feel bad', 'i feel terrible', 'i feel awful', 'i feel horrible',
                            'i feel lost', 'i feel empty', 'i feel broken', 'i feel hopeless',
                            'i feel worthless', 'i feel like giving up']
            },
            'Angry': {
                'words': ['angry', 'anger', 'furious', 'rage', 'hate', 'mad', 'annoyed', 'frustrated',
                          'irritated', 'outraged', 'bitter', 'hostile', 'aggressive', 'enraged',
                          'livid', 'infuriated', 'resentful', 'offended', 'despise', 'loathe', 'fuming'],
                'phrases': ['so angry', 'makes me mad', 'drives me crazy', 'fed up with', 'sick and tired',
                            'lost my temper', 'how dare', 'not fair', 'i am angry', 'i hate this',
                            'i hate everything', 'i hate my life', 'i feel angry']
            },
            'Anxious': {
                'words': ['anxious', 'anxiety', 'worried', 'nervous', 'scared', 'fear', 'afraid', 'panic',
                          'stress', 'stressed', 'tense', 'uneasy', 'dread', 'terror', 'frightened',
                          'insecure', 'overwhelmed', 'uncertain', 'paranoid', 'restless', 'overthinking'],
                'phrases': ['what if', 'cant breathe', 'heart racing', 'freaking out', 'losing my mind',
                            'so stressed', 'cant sleep', 'keep thinking', 'something bad',
                            'i feel anxious', 'i am anxious', 'i feel nervous', 'i feel scared',
                            'i feel worried', 'i am worried', 'i feel overwhelmed']
            },
            'Confused': {
                'words': ['confused', 'confusing', 'lost', 'unsure', 'uncertain', 'unclear', 'puzzled',
                          'baffled', 'clueless', 'stuck', 'blank', 'dazed', 'disoriented', 'mixed up'],
                'phrases': ["don't understand", "dont understand", "makes no sense", "no idea",
                            "what do i do", "i don't know", "i dont know", "not sure what",
                            "can't figure out", "cant figure out", "i feel confused", "i am confused",
                            "don't know what to do", "dont know what to do"]
            },
            'Lonely': {
                'words': ['lonely', 'alone', 'isolated', 'abandoned', 'forgotten', 'invisible',
                          'disconnected', 'excluded', 'unwanted', 'unloved', 'ignored', 'rejected'],
                'phrases': ['no one understands', 'no one cares', 'all by myself', 'feel invisible',
                            'no friends', 'nobody talks to me', 'no one to talk to', 'feel so alone',
                            'nobody loves me', 'i feel lonely', 'i am lonely', 'i feel alone']
            },
            'Hopeless': {
                'words': ['hopeless', 'worthless', 'useless', 'pointless', 'meaningless', 'doomed',
                          'trapped', 'suffocating', 'drowning', 'sinking', 'giving up'],
                'phrases': ['no hope', 'no future', 'no way out', 'nothing will change', 'nothing gets better',
                            'i feel hopeless', 'i feel worthless', 'i feel useless', 'i see no point',
                            'i feel trapped', 'i feel like giving up', 'i give up']
            }
        }

    def _detect_intensity(self, text_lower):
        for word in self.intensifiers['high']:
            if word in text_lower:
                return 'high'
        for word in self.intensifiers['medium']:
            if word in text_lower:
                return 'medium'
        for word in self.intensifiers['low']:
            if word in text_lower:
                return 'low'
        return 'medium'

    def _detect_sarcasm(self, text_lower):
        return any(re.search(p, text_lower) for p in self.sarcasm_patterns)

    def _contains_negation(self, words, idx):
        start = max(0, idx - 3)
        return any(w in self.negations for w in words[start:idx])

    def _get_boost(self, words, idx):
        start = max(0, idx - 2)
        for word in self.intensifiers['high']:
            if word in words[start:idx]:
                return 2.0
        for word in self.intensifiers['medium']:
            if word in words[start:idx]:
                return 1.5
        return 1.0

    def analyze(self, text, history=None):
        text_lower = text.lower().strip()
        text_lower = re.sub(r"['\u2019]", "'", text_lower)
        words = re.findall(r"\b\w+\b", text_lower)
        scores = {emotion: 0.0 for emotion in self.emotion_keywords}

        # violence / harm to others detection - highest priority
        for phrase in self.violence_phrases:
            if phrase in text_lower:
                return {
                    "emotion": "Violent", "intensity": "high",
                    "confidence": 99.0, "sarcasm": False,
                    "alert": "⚠️ Harming others is never the answer. Please step away and talk to someone you trust or call a helpline immediately."
                }

        # crisis detection
        for phrase in self.crisis_phrases:
            if phrase in text_lower:
                return {
                    "emotion": "Hopeless", "intensity": "high",
                    "confidence": 99.0, "sarcasm": False,
                    "alert": "⚠️ Please reach out to a mental health professional or call a helpline immediately. You are not alone."
                }

        # implicit sad
        for phrase in self.implicit_sad:
            if phrase in text_lower:
                scores['Sad'] += 3.0

        # phrase matching
        for emotion, data in self.emotion_keywords.items():
            for phrase in data['phrases']:
                if phrase in text_lower:
                    scores[emotion] += 2.0

        # word matching
        for idx, word in enumerate(words):
            for emotion, data in self.emotion_keywords.items():
                if word in data['words']:
                    if self._contains_negation(words, idx):
                        if emotion == 'Happy':
                            scores['Sad'] += 1.5
                        else:
                            scores[emotion] -= 0.5
                    else:
                        scores[emotion] += self._get_boost(words, idx)

        # context from history
        if history:
            last = history[-1].get('emotion', '')
            if last in scores:
                scores[last] += 0.5

        sarcasm = self._detect_sarcasm(text_lower)
        if sarcasm:
            scores['Happy'] = max(0, scores['Happy'] - 2)
            scores['Angry'] += 1.0

        top_emotion = max(scores, key=scores.get)
        top_score = scores[top_emotion]

        if top_score <= 0:
            negative_words = ['bad', 'wrong', 'terrible', 'horrible', 'awful', 'worst',
                               'hate', 'sick', 'tired', 'bored', 'ugh', 'blah']
            if any(w in words for w in negative_words):
                return {"emotion": "Sad", "intensity": "low", "confidence": 72.0, "sarcasm": False}
            return {"emotion": "Neutral", "intensity": "low", "confidence": 85.0, "sarcasm": False}

        positive_scores = {e: s for e, s in scores.items() if s > 0}
        total = sum(positive_scores.values())
        confidence = round((top_score / total) * 100, 2)
        confidence = max(min(confidence, 99.0), 55.0)

        return {
            "emotion": top_emotion,
            "intensity": self._detect_intensity(text_lower),
            "confidence": confidence,
            "sarcasm": sarcasm
        }
