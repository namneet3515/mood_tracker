from flask import Flask, render_template, request
from mood_detector import detect_mood  # Import the detect_mood function
from flask import Flask, render_template, request, redirect, url_for, flash
from mood_detector import detect_mood
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the main page with the form

app.secret_key = 'your_secret_key_here'  # Required for flash messages

# MOOD_ARTICLES dictionary with titles, snippets, and reading times
MOOD_ARTICLES = {
    "Happy": [
        {"title": "10 Ways to Stay Happy", "snippet": "Discover simple habits to maintain your happiness.", "reading_time": "3 min"},
        {"title": "The Science of Happiness", "snippet": "Explore what science says about being happy.", "reading_time": "5 min"},
        {"title": "How to Spread Joy", "snippet": "Share your happiness with those around you.", "reading_time": "4 min"}
    ],
    "Sad": [
        {"title": "Coping with Sadness", "snippet": "Learn techniques to help you deal with sadness.", "reading_time": "4 min"},
        {"title": "Ways to Lift Your Mood", "snippet": "Quick tips to turn a sad day into a good one.", "reading_time": "3 min"},
        {"title": "Talking About Feelings", "snippet": "Why expressing emotions can help.", "reading_time": "5 min"}
    ],
    "Neutral": [
        {"title": "Finding Balance in Life", "snippet": "Achieve balance and clarity in your day.", "reading_time": "4 min"},
        {"title": "The Benefits of Mindfulness", "snippet": "Learn how mindfulness improves mental well-being.", "reading_time": "5 min"},
        {"title": "Living in the Present", "snippet": "Why focusing on now leads to joy.", "reading_time": "3 min"}
    ],
    "Stressed": [
        {"title": "How to Relieve Stress", "snippet": "Practical steps to feel more relaxed.", "reading_time": "4 min"},
        {"title": "Managing Stress in Everyday Life", "snippet": "Tips to keep stress at bay during a busy day.", "reading_time": "5 min"},
        {"title": "Relaxation Techniques", "snippet": "Quick ways to unwind and recharge.", "reading_time": "3 min"}
    ]
}



@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        user_input = request.form['mood_input']
        mood = detect_mood(user_input)
        
        if mood not in MOOD_ARTICLES:
            flash("Mood not recognized. Defaulting to 'Neutral'.")
            mood = "Neutral"
        
        # Define activities for each mood
        activities = {
            "Happy": [
                'Share your joy with others through a kind gesture!',
                'Take some fun photos to capture this great mood',
                'Start a gratitude journal to remember this feeling'
            ],
            "Sad": [
                'Watch some funny cat videos - they always help!',
                'Try some light exercise to boost your mood',
                'Call a friend for a cheerful chat'
            ],
            "Neutral": [
                'How about trying a new hobby today?',
                'Take a refreshing walk outside',
                'Listen to your favorite upbeat playlist'
            ],
            "Stressed": [
                'Take a few minutes for deep breathing',
                'Watch a funny video to lighten your mood',
                'Step outside for some fresh air'
            ]
        }.get(mood, [])
        
        # Get random articles for the current mood
        articles = random.sample(MOOD_ARTICLES[mood], 2)

        return render_template('result.html', 
                               mood=mood, 
                               activities=activities, 
                               articles=articles)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        journal_entry = request.form.get('journal_entry')
        mood = request.form.get('mood')
        
        # Flash success message (simulates saving to a database)
        flash("Your journal entry has been saved successfully!")
        
        if mood not in MOOD_ARTICLES:
            flash("Mood not recognized. Defaulting to 'Neutral'.")
            mood = "Neutral"
        
        # Define activities for each mood
        activities = {
            "Happy": [
                'Share your joy with others through a kind gesture!',
                'Take some fun photos to capture this great mood',
                'Start a gratitude journal to remember this feeling'
            ],
            "Sad": [
                'Watch some funny cat videos - they always help!',
                'Try some light exercise to boost your mood',
                'Call a friend for a cheerful chat'
            ],
            "Neutral": [
                'How about trying a new hobby today?',
                'Take a refreshing walk outside',
                'Listen to your favorite upbeat playlist'
            ],
            "Stressed": [
                'Take a few minutes for deep breathing',
                'Watch a funny video to lighten your mood',
                'Step outside for some fresh air'
            ]
        }.get(mood, [])
        
        articles = random.sample(MOOD_ARTICLES[mood], 2)
        
        return render_template('result.html', 
                               mood=mood, 
                               activities=activities, 
                               articles=articles,
                               journal_success=True)

if __name__ == "__main__":
    app.run(debug=True)

