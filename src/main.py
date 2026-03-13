from emotion_analyzer import EmotionAnalyzer

def main():
    analyzer = EmotionAnalyzer()
    print("=== Emotion Analyzer AI ===\n")
    
    while True:
        text = input("Enter text to analyze (or 'quit' to exit): ").strip()
        if text.lower() == 'quit':
            break
        if not text:
            continue
            
        result = analyzer.analyze(text)
        print(f"Emotion: {result['emotion']}")
        print(f"Confidence: {result['confidence']}%\n")

if __name__ == "__main__":
    main()
