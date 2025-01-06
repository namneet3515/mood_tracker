from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
import re

# Download required NLTK data
nltk.download('punkt')

class MoodDetector:
    def __init__(self):
        self.mood_keywords = {
            'anxiety': ['worried', 'nervous', 'anxious', 'fear', 'panic', 'stress', 'tense', 'uneasy'],
            'depression': ['sad', 'hopeless', 'worthless', 'empty', 'tired', 'alone', 'depressed', 'exhausted'],
            'stress': ['overwhelmed', 'pressure', 'busy', 'frustrated', 'deadline', 'overworked', 'burden'],
            'positive': ['happy', 'excited', 'grateful', 'peaceful', 'relaxed', 'joy', 'confident', 'optimistic']
        }

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text.strip()

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }

    def detect_mood_keywords(self, text):
        import nltk
        nltk.data.path.append(r'C:/Users/NAMNEET/nltk_data')  # Specify the path to the NLTK data folder

# If necessary, download punkt from that path
        nltk.download('punkt', download_dir=r'C:/Users/NAMNEET/nltk_data')
        text = self.preprocess_text(text)   
        words = word_tokenize(text)
        mood_scores = {mood: 0 for mood in self.mood_keywords.keys()}
        for word in words:
            for mood, keywords in self.mood_keywords.items():
                if word in keywords:
                    mood_scores[mood] += 1
        return mood_scores

    def analyze_mood(self, text):
        cleaned_text = self.preprocess_text(text)
        sentiment = self.analyze_sentiment(cleaned_text)
        mood_scores = self.detect_mood_keywords(cleaned_text)
        primary_mood = max(mood_scores.items(), key=lambda x: x[1])[0] if any(mood_scores.values()) else 'neutral'

        return {
            'primary_mood': primary_mood,
            'sentiment_polarity': sentiment['polarity'],
            'sentiment_subjectivity': sentiment['subjectivity'],
            'mood_indicators': mood_scores
        }
