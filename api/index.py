from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotion_analyzer import EmotionAnalyzer

app = Flask(__name__, template_folder='../src/templates', static_folder='../src/static')
analyzer = None

def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = EmotionAnalyzer()
    return analyzer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    result = get_analyzer().analyze(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
