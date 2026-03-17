const emotionEmojis = {
    'Happy': '😊',
    'Sad': '😢',
    'Angry': '😠',
    'Anxious': '😰',
    'Excited': '🤩',
    'Disgusted': '🤢',
    'Neutral': '😐'
};

async function analyzeEmotion() {
    const text = document.getElementById('textInput').value.trim();
    
    if (!text) {
        alert('Please enter some text to analyze');
        return;
    }
    
    document.getElementById('result').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        displayResult(data);
    } catch (error) {
        alert('Error analyzing emotion: ' + error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

function displayResult(data) {
    const emotion = data.emotion;
    const confidence = data.confidence;
    
    document.getElementById('emotionIcon').textContent = emotionEmojis[emotion] || '🤔';
    document.getElementById('emotionText').textContent = emotion;
    document.getElementById('emotionText').className = `emotion-${emotion}`;
    document.getElementById('confidenceText').textContent = `${confidence}%`;
    document.getElementById('progressFill').style.width = `${confidence}%`;

    const alertBox = document.getElementById('alertBox');
    if (data.alert) {
        alertBox.textContent = data.alert;
        alertBox.classList.remove('hidden');
    } else {
        alertBox.classList.add('hidden');
    }
    
    document.getElementById('result').classList.remove('hidden');
}

document.getElementById('textInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        analyzeEmotion();
    }
});
