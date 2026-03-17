from flask import Flask, render_template, request, jsonify, session
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotion_analyzer import EmotionAnalyzer
from response_engine import ResponseEngine

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'src', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'src', 'static'))

app.secret_key = 'emotion-ai-secret-key'

analyzer = EmotionAnalyzer()
engine = ResponseEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    text = data.get('text', '').strip()
    history = data.get('history', [])

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    result = analyzer.analyze(text, history)
    reply = engine.generate(result['emotion'], result['intensity'], result['sarcasm'], history)

    return jsonify({
        "emotion": result['emotion'],
        "intensity": result['intensity'],
        "confidence": result['confidence'],
        "sarcasm": result['sarcasm'],
        "response": reply['response'],
        "suggestion": reply['suggestion'],
        "followup": reply['followup'],
        "alert": result.get('alert')
    })

if __name__ == '__main__':
    app.run(debug=True)
