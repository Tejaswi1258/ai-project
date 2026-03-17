import random

class ResponseEngine:
    def __init__(self):
        self.responses = {
            'Happy': {
                'low':    ["That's really nice to hear! What's been making you feel good?",
                           "Glad things are going well for you! Keep that energy going 😊"],
                'medium': ["Love that! Sounds like things are going really well for you.",
                           "That's wonderful! It's great when life feels this good."],
                'high':   ["That's amazing! You sound absolutely on top of the world right now 🌟",
                           "Yes!! That energy is contagious — so happy for you! 🎉"]
            },
            'Excited': {
                'low':    ["Oh nice, something good coming up? Tell me more!",
                           "Sounds like you've got something to look forward to!"],
                'medium': ["That's so exciting! What's got you feeling this way?",
                           "I can feel the excitement! What's happening?"],
                'high':   ["Okay I love this energy!! What's going on?! 🤩",
                           "You're buzzing right now and honestly it's amazing — what happened?!"]
            },
            'Sad': {
                'low':    ["Hey, it sounds like things are a bit heavy right now. Want to talk about it?",
                           "I'm here. Sometimes just getting it out helps — what's going on?"],
                'medium': ["I'm really sorry you're feeling this way. That sounds genuinely tough.",
                           "That sounds really hard. You don't have to carry that alone — I'm listening."],
                'high':   ["I'm so sorry. What you're feeling right now sounds overwhelming, and that's okay to feel.",
                           "That sounds incredibly painful. Please know you're not alone in this — I'm right here with you."]
            },
            'Angry': {
                'low':    ["Sounds like something's been bugging you. What happened?",
                           "I get it — some things are just frustrating. Want to vent?"],
                'medium': ["That sounds really frustrating. It makes sense you'd feel that way.",
                           "I hear you. When things feel unfair it's hard not to get angry. What's going on?"],
                'high':   ["Wow, that sounds like it really got to you — and honestly, I get why.",
                           "That level of anger usually means something really crossed a line. I'm listening."]
            },
            'Anxious': {
                'low':    ["Sounds like something's on your mind. Want to talk through it?",
                           "A little worry is normal — what's been on your mind lately?"],
                'medium': ["I can hear that you're stressed. Take a breath — let's work through this together.",
                           "That sounds like a lot to carry. You don't have to figure it all out at once."],
                'high':   ["Hey, slow down for a second. You're safe right now. Take a deep breath with me.",
                           "That sounds really overwhelming. Let's take it one thing at a time — what's the biggest thing worrying you?"]
            },
            'Confused': {
                'low':    ["Not sure what to make of it? That's totally okay — let's think it through.",
                           "Sometimes things just don't make sense at first. What's confusing you?"],
                'medium': ["I get why that feels unclear. Let's break it down together — what part is tripping you up?",
                           "Confusion usually means you're thinking deeply about something. What's going on?"],
                'high':   ["Okay, sounds like a lot is tangled up right now. Let's slow down and untangle it piece by piece.",
                           "That sounds genuinely overwhelming to process. Let's start with the simplest part — what do you know for sure?"]
            },
            'Lonely': {
                'low':    ["Sometimes it just feels quieter than you'd like, huh? I'm here.",
                           "Feeling a bit disconnected? That happens — want to talk?"],
                'medium': ["Loneliness can feel really heavy. I'm glad you're talking — even this counts.",
                           "I hear you. Feeling unseen or alone is one of the hardest feelings. I'm here with you."],
                'high':   ["I'm really sorry you're feeling this alone. That kind of emptiness is real and it hurts.",
                           "You reached out, and that matters. You're not invisible — I see you, and I'm here."]
            },
            'Hopeless': {
                'low':    ["It sounds like things feel stuck right now. That feeling won't last forever.",
                           "When nothing feels worth it, it's hard to see a way forward. But you're still here — that matters."],
                'medium': ["I hear how exhausted and hopeless you feel. Please don't give up — things can shift.",
                           "That kind of hopelessness is heavy. You don't have to fix everything today. Just stay with me."],
                'high':   ["Please hear me — what you're feeling is real, but you matter more than you know right now.",
                           "I'm really concerned about you. Please talk to someone you trust or call a helpline. You deserve support. 💙"]
            },
            'Neutral': {
                'low':    ["Hey! How are you doing today?",
                           "What's on your mind?"],
                'medium': ["Seems like a calm day. Anything you want to talk about?",
                           "I'm here — feel free to share whatever's on your mind."],
                'high':   ["I'm here and listening. What would you like to talk about?",
                           "Sometimes neutral is good. What's going on with you today?"]
            }
        }

        self.suggestions = {
            'Sad': [
                "Try doing one small thing that usually brings you comfort — even something tiny counts.",
                "Sometimes writing down how you feel helps get it out of your head.",
                "Reach out to someone you trust today, even just to say hi.",
                "Be gentle with yourself right now. You don't have to be okay all the time."
            ],
            'Angry': [
                "Try stepping away for a few minutes before reacting — even a short walk helps.",
                "Write down exactly what made you angry — sometimes seeing it on paper helps.",
                "Take 5 slow deep breaths. It sounds simple but it genuinely works.",
                "Ask yourself: will this matter in a week? It helps put things in perspective."
            ],
            'Anxious': [
                "Try the 5-4-3-2-1 technique: name 5 things you see, 4 you hear, 3 you can touch.",
                "Focus only on what you can control right now — let go of the rest for a moment.",
                "Write down your worries and next to each one write: 'can I control this?'",
                "Take slow deep breaths — inhale for 4 counts, hold for 4, exhale for 6."
            ],
            'Confused': [
                "Try writing down what you know vs what you don't — it helps separate the noise.",
                "Break the problem into the smallest possible pieces and tackle one at a time.",
                "Sometimes sleeping on it genuinely helps — your brain keeps working in the background.",
                "Talk it out loud, even to yourself — hearing it often makes it clearer."
            ],
            'Lonely': [
                "Send a message to someone you haven't talked to in a while — even a simple 'hey'.",
                "Try joining an online community around something you enjoy.",
                "Sometimes being around people, even strangers in a café, helps ease the feeling.",
                "Remember: loneliness is a feeling, not a fact. People do care about you."
            ],
            'Hopeless': [
                "Please talk to someone you trust about how you're feeling.",
                "Call or text a mental health helpline — they're there for exactly this.",
                "Focus on just the next hour, not the big picture. One hour at a time.",
                "You've made it through hard times before. This feeling is not permanent."
            ]
        }

        self.sarcasm_responses = [
            "I'm sensing that might not be as great as it sounds — what's really going on?",
            "Something tells me things aren't quite as fine as you're making out. Want to talk?",
            "I hear you, but I also hear what you're not saying. What's actually up?"
        ]

        self.followups = {
            'Sad':      ["What's been the hardest part of your day?", "How long have you been feeling this way?", "Is there anything specific that triggered this?"],
            'Angry':    ["What happened that set this off?", "Has this been building up for a while?", "Who or what is this directed at, if you don't mind sharing?"],
            'Anxious':  ["What's the main thing you're worried about right now?", "Is this a new feeling or has it been around for a while?", "What usually helps you calm down?"],
            'Confused': ["What part is the most unclear to you?", "What do you already know about the situation?", "What outcome are you hoping for?"],
            'Lonely':   ["When did you start feeling this way?", "Is there someone specific you're missing?", "What kind of connection are you craving right now?"],
            'Hopeless': ["What's made you feel this way?", "Is there one small thing that used to bring you comfort?", "Have you been able to talk to anyone about this?"],
            'Happy':    ["What's been the highlight of your day?", "What made this happen?", "How long have you been feeling this good?"],
            'Excited':  ["What's the big thing you're looking forward to?", "How long have you been waiting for this?", "Who are you sharing this excitement with?"],
            'Neutral':  ["Anything on your mind today?", "How has your day been going?", "Anything you want to talk through?"]
        }

    def generate(self, emotion, intensity, sarcasm, history=None):
        if sarcasm:
            response = random.choice(self.sarcasm_responses)
            return {"response": response, "suggestion": None, "followup": None}

        emotion_responses = self.responses.get(emotion, self.responses['Neutral'])
        intensity_responses = emotion_responses.get(intensity, emotion_responses.get('medium'))
        response = random.choice(intensity_responses)

        suggestion = None
        if emotion in self.suggestions and intensity in ['medium', 'high']:
            suggestion = random.choice(self.suggestions[emotion])

        followup = None
        if emotion in self.followups:
            followup = random.choice(self.followups[emotion])

        return {
            "response": response,
            "suggestion": suggestion,
            "followup": followup
        }
