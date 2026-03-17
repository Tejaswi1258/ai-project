from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotion_analyzer import EmotionAnalyzer

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'src', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'src', 'static'))

analyzer = EmotionAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    result = analyzer.analyze(text)
    return jsonify(result)
