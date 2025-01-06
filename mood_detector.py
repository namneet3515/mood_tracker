# mood_detector.py

from textblob import TextBlob

def detect_mood(text):
    """
    Detects the mood of the user based on the sentiment of the entered text.
    It uses TextBlob for sentiment analysis and categorizes the mood into four types:
    - Happy
    - Sad
    - Neutral
    - Stressed
    """
    # Perform sentiment analysis using TextBlob
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Mood determination based on polarity score
    if polarity > 0.2:
        return 'Happy'
    elif polarity < -0.2:
        return 'Sad'
    elif polarity == 0:
        return 'Neutral'
    else:
        return 'Stressed'
