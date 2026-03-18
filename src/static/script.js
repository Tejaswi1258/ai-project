const emotionEmojis = {
    Happy: '😊', Excited: '🤩', Sad: '😢', Angry: '😠',
    Anxious: '😰', Confused: '😕', Lonely: '😔', Hopeless: '💙', Violent: '🚨', Neutral: '😐'
};

let history = [];

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function addMessage(text, role) {
    const window = document.getElementById('chatWindow');
    const div = document.createElement('div');
    div.className = `message ${role === 'user' ? 'user-message' : 'ai-message'}`;
    div.innerHTML = `
        <span class="avatar">${role === 'user' ? '🧑' : '🧠'}</span>
        <div class="bubble">${text}</div>
    `;
    window.appendChild(div);
    window.scrollTop = window.scrollHeight;
    return div;
}

function showTyping() {
    const window = document.getElementById('chatWindow');
    const div = document.createElement('div');
    div.className = 'message ai-message typing-msg';
    div.innerHTML = `
        <span class="avatar">🧠</span>
        <div class="bubble typing">
            <div class="typing-dots"><span></span><span></span><span></span></div>
        </div>
    `;
    window.appendChild(div);
    window.scrollTop = window.scrollHeight;
    return div;
}

function addAIResponse(data) {
    const chatWindow = document.getElementById('chatWindow');
    const div = document.createElement('div');
    div.className = 'message ai-message';

    const emoji = emotionEmojis[data.emotion] || '🤔';
    const intensity = data.intensity || 'medium';

    let html = `
        <span class="avatar">🧠</span>
        <div>
            <div class="bubble">${data.response}</div>
            <span class="emotion-badge badge-${data.emotion}">${emoji} ${data.emotion} · ${intensity}</span>
    `;

    if (data.suggestion) {
        html += `<div class="suggestion-card">💡 ${data.suggestion}</div>`;
    }

    if (data.followup) {
        html += `<div class="followup">${data.followup}</div>`;
    }

    html += `</div>`;
    div.innerHTML = html;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function updateSidebar(emotion, text) {
    const history = document.getElementById('emotionHistory');
    const item = document.createElement('div');
    item.className = 'history-item';
    const emoji = emotionEmojis[emotion] || '🤔';
    const short = text.length > 22 ? text.substring(0, 22) + '…' : text;
    item.innerHTML = `<span>${emoji}</span><span>${short}</span>`;
    history.appendChild(item);

    document.getElementById('currentEmotion').textContent = `${emoji} ${emotion}`;
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    input.style.height = 'auto';
    document.getElementById('sendBtn').disabled = true;

    addMessage(text, 'user');
    const typingEl = showTyping();

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, history })
        });

        const data = await res.json();
        typingEl.remove();

        if (data.error) {
            addMessage('Something went wrong. Try again.', 'ai');
            return;
        }

        const alertBanner = document.getElementById('alertBanner');
        if (data.alert) {
            alertBanner.textContent = data.alert;
            alertBanner.classList.remove('hidden');
        } else {
            alertBanner.classList.add('hidden');
        }

        addAIResponse(data);
        updateSidebar(data.emotion, text);

        history.push({ role: 'user', text, emotion: data.emotion });
        if (history.length > 10) history.shift();

    } catch (err) {
        typingEl.remove();
        addMessage('Something went wrong. Please try again.', 'ai');
    } finally {
        document.getElementById('sendBtn').disabled = false;
    }
}

function clearChat() {
    history = [];
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.innerHTML = `
        <div class="message ai-message">
            <span class="avatar">🧠</span>
            <div class="bubble">Hey there! I'm EmoAI — I'm here to listen and understand how you're really feeling. What's on your mind today?</div>
        </div>
    `;
    document.getElementById('emotionHistory').innerHTML = '<p class="history-label">Emotion History</p>';
    document.getElementById('currentEmotion').textContent = '';
    document.getElementById('alertBanner').classList.add('hidden');
}

document.getElementById('userInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
