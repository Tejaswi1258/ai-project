# Emotion Analyzer AI

An AI-powered emotion classification system with a modern web interface. Analyzes text to detect emotions like Happy, Sad, Angry, Anxious, Excited, and more.

## Features
- Multi-class emotion detection (Happy, Sad, Angry, Anxious, Excited, Disgusted, Neutral)
- Pre-trained emotion classification model
- Modern web interface with real-time analysis
- Confidence scores with visual progress bars
- Emoji-based emotion display

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)
1. Start the Flask server:
```bash
cd src
python app.py
```

2. Open your browser and go to:
```
http://localhost:5000
```

3. Enter text and click "Analyze Emotion"

### Command Line Interface
```bash
cd src
python main.py
```

## Examples
- "I'm so excited about this project!" → **Excited**
- "I feel alone and isolated" → **Sad**
- "This makes me so angry!" → **Angry**
- "I'm worried about tomorrow" → **Anxious**
- "Everything is going great!" → **Happy**

## Model
Uses the pre-trained `emotion-english-distilroberta-base` model trained on emotion classification tasks.

## Requirements
- Python 3.8+
- transformers
- torch
- flask
