from flask import Flask, render_template, request
from mood_detector import detect_mood  # Import the detect_mood function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the main page with the form

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        # Get the text input from the form
        user_input = request.form['mood_input']
        
        # Call the detect_mood function to determine the mood
        mood = detect_mood(user_input)
        
        # Provide personalized wellness recommendations based on the mood
        if mood == 'Happy':
            activities = ['Listen to uplifting music', 'Practice gratitude', 'Call a friend']
        elif mood == 'Sad':
            activities = ['Try deep breathing exercises', 'Watch a comedy movie', 'Read a positive book']
        elif mood == 'Neutral':
            activities = ['Go for a walk', 'Try journaling', 'Do some light exercise']
        else:  # If mood is stressed or other negative mood
            activities = ['Practice mindfulness meditation', 'Try some light exercise', 'Try relaxation techniques']

        # Render the result page with the detected mood and suggested activities
        return render_template('result.html', mood=mood, activities=activities)

if __name__ == "__main__":
    app.run(debug=True)
