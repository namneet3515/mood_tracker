import nltk
nltk.data.path.append(r'C:/Users/NAMNEET/nltk_data')  # Adjust path if necessary

# Download the correct resource
nltk.download('punkt', download_dir=r'C:/Users/NAMNEET/nltk_data')

from flask import Flask, render_template, request
from mood_detector import MoodDetector

app = Flask(__name__)
mood_detector = MoodDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form['mood_input']
    result = mood_detector.analyze_mood(user_input)

    return render_template('result.html', mood=result['primary_mood'], analysis=result)

if __name__ == '__main__':
    app.run(debug=True)
