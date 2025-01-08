from flask import Flask, render_template, request, redirect, url_for, flash
from mood_detector import detect_mood
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Emergency resources
EMERGENCY_RESOURCES = {
    "hotlines": [
        {"name": "National Suicide Prevention Lifeline", "number": "988"},
        {"name": "Crisis Text Line", "contact": "Text HOME to 741741"},
        {"name": "Emergency Services", "number": "911"}
    ],
    "immediate_actions": [
        "Take slow, deep breaths",
        "Know that you're not alone",
        "Stay with someone if possible",
        "Remove any harmful objects"
    ],
    "support_resources": [
        {"name": "Find a Therapist", "link": "https://www.psychologytoday.com/us/therapists"},
        {"name": "Online Support Groups", "link": "https://www.nami.org/Support-Education/Support-Groups"},
        {"name": "Mental Health America", "link": "https://mhanational.org/finding-help"}
    ]
}

# Mood-specific articles and resources
MOOD_ARTICLES = {
    "Happy": [
        {"title": "10 Ways to Maintain Joy", "snippet": "Discover simple habits to maintain your happiness.", "reading_time": "3 min"},
        {"title": "The Science of Happiness", "snippet": "Explore what science says about being happy.", "reading_time": "5 min"},
        {"title": "How to Spread Joy", "snippet": "Share your happiness with those around you.", "reading_time": "4 min"}
    ],
    "Depressed": [
        {"title": "Coping with Depression", "snippet": "Learn effective techniques for managing depression.", "reading_time": "4 min"},
        {"title": "Finding Hope Again", "snippet": "Steps to help you through difficult times.", "reading_time": "5 min"},
        {"title": "Professional Help Guide", "snippet": "When and how to seek professional support.", "reading_time": "6 min"},
        {"title": "Self-Care Basics", "snippet": "Essential self-care practices for tough days.", "reading_time": "3 min"}
    ],
    "Neutral": [
        {"title": "Finding Balance in Life", "snippet": "Achieve balance and clarity in your day.", "reading_time": "4 min"},
        {"title": "The Benefits of Mindfulness", "snippet": "Learn how mindfulness improves mental well-being.", "reading_time": "5 min"},
        {"title": "Living in the Present", "snippet": "Why focusing on now leads to joy.", "reading_time": "3 min"}
    ],
    "Stressed": [
        {"title": "Stress Management 101", "snippet": "Practical steps to feel more relaxed.", "reading_time": "4 min"},
        {"title": "Quick Anxiety Relief", "snippet": "Immediate techniques for managing stress.", "reading_time": "3 min"},
        {"title": "Understanding Stress", "snippet": "Learn about stress and how to manage it.", "reading_time": "5 min"},
        {"title": "Relaxation Techniques", "snippet": "Proven methods to unwind and recharge.", "reading_time": "4 min"}
    ]
}

# Mood-specific activities
ACTIVITIES = {
    "Happy": [
        'Share your joy with others through a kind gesture!',
        'Take some fun photos to capture this great mood',
        'Start a gratitude journal to remember this feeling',
        'Try a new hobby while your energy is high'
    ],
    "Depressed": [
        'Take small, manageable steps - one thing at a time',
        'Reach out to a trusted friend or family member',
        'Consider talking to a mental health professional',
        'Try gentle exercise like a short walk',
        'Remember you are not alone in this feeling'
    ],
    "Neutral": [
        'How about trying a new hobby today?',
        'Take a refreshing walk outside',
        'Listen to your favorite upbeat playlist',
        'Practice mindfulness meditation'
    ],
    "Stressed": [
        'Take a few deep, calming breaths',
        'Try progressive muscle relaxation',
        'Step outside for some fresh air',
        'Write down what is on your mind',
        'Take a break from screens for 30 minutes'
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        user_input = request.form['mood_input']
        mood = detect_mood(user_input)
        
        if mood == 'Emergency':
            # Log the emergency case (implement secure logging in production)
            with open('emergency_log.txt', 'a') as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"Emergency detected at {timestamp}\n")
            
            return render_template('emergency.html',
                                 resources=EMERGENCY_RESOURCES,
                                 original_text=user_input)
        
        if mood not in MOOD_ARTICLES:
            flash("Mood not recognized. Showing general wellness resources.")
            mood = "Neutral"
        
        articles = random.sample(MOOD_ARTICLES[mood], min(2, len(MOOD_ARTICLES[mood])))
        activities = random.sample(ACTIVITIES[mood], min(3, len(ACTIVITIES[mood])))
        
        return render_template('result.html', 
                             mood=mood, 
                             activities=activities, 
                             articles=articles)

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        journal_entry = request.form.get('journal_entry')
        mood = request.form.get('mood')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Write to the journal file
        with open('journal.txt', 'a') as file:
            file.write(f"Date & Time: {timestamp}\n")
            file.write(f"Mood: {mood}\n")
            file.write(f"Entry: {journal_entry}\n\n")
        
        flash("Your journal entry has been saved successfully!")

        if mood not in MOOD_ARTICLES:
            flash("Mood not recognized. Showing general wellness resources.")
            mood = "Neutral"
        
        articles = random.sample(MOOD_ARTICLES[mood], min(2, len(MOOD_ARTICLES[mood])))
        activities = random.sample(ACTIVITIES[mood], min(3, len(ACTIVITIES[mood])))
        
        return render_template('result.html', 
                             mood=mood, 
                             activities=activities, 
                             articles=articles,
                             journal_success=True)

@app.route('/get_help', methods=['POST'])
def get_help():
    if request.method == 'POST':
        name = request.form.get('name', 'Anonymous')
        contact = request.form.get('contact', '')
        consent = request.form.get('consent', False)
        
        if consent:
            # Log the help request (implement secure logging in production)
            with open('help_requests.txt', 'a') as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"Help requested at {timestamp}\n")
                file.write(f"Name: {name}\nContact: {contact}\n\n")
            
            flash("Thank you for reaching out. A mental health professional will contact you soon.")
        else:
            flash("Please provide consent for us to help you.")
        
        return render_template('emergency.html',
                             resources=EMERGENCY_RESOURCES,
                             show_confirmation=True)

if __name__ == "__main__":
    app.run(debug=True)