from textblob import TextBlob
import re

def is_negated(phrase: str, text: str) -> bool:
    """
    Checks for negation of the phrase in the given text.
    """
    negation_words = {
        'not', "don't", "doesn't", "didn't", "never", "no", 
        "wasn't", "weren't", "isn't", "aren't", "none", 
        "nothing", "nowhere", "neither", "nor", "cannot"
    }

    phrase_positions = [m.start() for m in re.finditer(re.escape(phrase), text)]
    
    for pos in phrase_positions:
        before_text = text[:pos].split()[-5:]
        if any(neg in before_text for neg in negation_words):
            return True
    
    return False

def detect_mood(text):
    """
    Detects the mood of the user based on the sentiment of the entered text.
    Includes emergency detection for suicidal ideation and negation handling.
    """
    # Emergency keywords that indicate potential crisis
    emergency_keywords = {
    'suicide': 3, 'suicidal': 3, 'kill myself': 3, 'want to die': 3, 'end my life': 3,
    'no reason to live': 3, 'better off dead': 3, 'cant go on': 2, 'worthless': 2,
    'everyone would be better without me': 3, 'goodbye forever': 2, 'end it all': 3,
    'final note': 3, 'take my life': 3, 'self-harm': 2, 'cut myself': 3, 'end my suffering': 3,
    'death is the answer': 3, 'i want to die': 3, 'i can’t go on': 2, 'nothing left to live for': 3,
    'life is not worth it': 3, 'in unbearable pain': 3, 'wish I was never born': 3, 'it will never get better': 3,
    'i feel like i’m dying': 3, 'i am broken': 2, 'i don’t deserve to live': 3, 'i’m useless': 2,
    'i can’t take it anymore': 3, 'this pain won’t stop': 3, 'i want to end it all': 3, 'i have nothing to live for': 3,
    'i don’t want to be here anymore': 3, 'nobody cares': 2, 'i don’t matter': 2, 'no one will miss me': 2,
    'no hope left': 3, 'i’m so alone': 2, 'goodbye cruel world': 3, 'i’m at the end of my rope': 3, 
    'i can’t handle this': 3, 'i’m tired of living': 3, 'i don’t see a way out': 3, 'everything is pointless': 3, 
    'i am just a burden': 2, 'no escape from this pain': 3, 'it’s not worth fighting anymore': 3, 
    'nobody will care if i’m gone': 3, 'life isn’t worth living': 3, 'i’m too weak to go on': 3, 
    'death is the only way out': 3, 'i am a failure': 2, 'nobody loves me': 2, 'i am invisible': 2, 
    'i have failed everyone': 2, 'i wish I could disappear': 3, 'i can’t do this anymore': 3, 'no one understands': 2,
    'i don’t want help': 3, 'my life has no meaning': 3, 'i feel empty': 2, 'i’m just a mistake': 2, 
    'there’s no way out': 3, 'i’m lost': 2, 'it’s too late for me': 3, 'life is not worth living anymore': 3,
    'i’m exhausted': 2, 'i want to escape': 3, 'i’m not strong enough': 2, 'i’m trapped in my own mind': 2,
    'i want to be gone': 3, 'i’m too broken to fix': 2, 'there is no future for me': 3, 'i don’t fit in this world': 2,
    'there’s no reason to go on': 3, 'i am stuck in this pain': 3, 'i want peace': 3, 'no way out of this pain': 3,
    'i feel hopeless': 2, 'my mind is my enemy': 2, 'it’s all too much': 3, 'this is too much to handle': 3,
    'i don’t want to be a burden': 2, 'nobody will ever know': 2, 'it’s all my fault': 2, 'i’m done fighting': 3,
    'my existence is a mistake': 2, 'nobody will care when I’m gone': 2, 'i want it to stop': 3, 'i am drowning': 3,
    'i feel suffocated': 2, 'i don’t care anymore': 3, 'i’ve had enough': 3, 'life is too painful': 3, 
    'i wish I could sleep forever': 3, 'i want to fade away': 3, 'no one will miss me when I’m gone': 2,
    'everything hurts': 2, 'the world is better off without me': 3, 'nobody would care if I was gone': 3,
    'I don’t see the point of life': 3, 'there’s no point to any of this': 3, 'I’ve lost everything': 3,
    'I’m too far gone': 3, 'I just want peace': 3, 'I’m done with life': 3, 'life is a burden': 3, 'I want to escape this pain': 3,
    'kill': 3, 'killed': 3, 'dying': 3, 'dead': 3, 'death': 3, 'end': 3, 'end it': 3, 'end me': 3,
    'marne': 3, 'marna': 3, 'khudkhushi': 3, 'faansi': 3, 'aatma hatya': 2, 'jeevan tyaag': 2
}



    # Expanded keyword lists with weights
    mood_keywords = {
        'Depressed': {
            'Depressed': {
    'depressed': 3, 'hopeless': 3, 'worthless': 3, 'empty': 2, 
    'down': 2, 'blue': 2, 'sinking': 2, 'isolated': 2, 
    'alone': 2, 'sad': 2, 'miserable': 2, 'terrible': 2, 
    'awful': 2, 'lonely': 2, 'crying': 2, 'heartbroken': 3, 
    'lost': 2, 'devastated': 3, 'gloomy': 2, 'broken': 2, 
    'unwanted': 2, 'forgotten': 2, 'worthless': 3, 'defeated': 2,
    'dreadful': 2, 'melancholy': 3, 'weary': 2, 'despair': 3, 
    'unloved': 2, 'numb': 2, 'desolate': 3, 'grief': 3, 
    'mourning': 2, 'pained': 2,
    # Adding more English and Hindi words
    'downhearted': 3, 'disheartened': 3, 'forsaken': 3, 'empty inside': 3, 
    'broken hearted': 3, 'abandoned': 3, 'hopelessness': 3, 'grief-stricken': 3, 
    'tearful': 2, 'despondent': 3, 'sorrowful': 3, 'heartache': 3, 
    'dismayed': 2, 'mournful': 3, 'dejection': 3, 'tragic': 3, 
    'hurt': 2, 'sick at heart': 2, 'morose': 3, 'unhappy': 2, 
    'aching': 2, 'shattered': 3, 'woe': 3, 'down in the dumps': 3, 
    'longing': 2, 'dispirited': 3, 'detached': 2, 'sorrow': 3, 
    'anguish': 3, 'bleak': 3, 'abandoned soul': 3, 'without hope': 3,
    # Hindi transliterations
    'udaseen': 3, 'nirash': 3, 'bekaar': 3, 'khali': 2, 
    'piche': 2, 'dukh': 2, 'shok': 3, 'akela': 2, 
    'veera': 2, 'bikhra hua': 3, 'tanha': 2, 'dukh bhara': 3,
    'nasamajh': 2, 'vishaal dard': 3, 'nirash man': 3, 'faaltu': 2,
    'dard bhara': 2, 'akela pan': 2, 'dard se bhara': 2, 'dukhbhari': 2, 
    'shokh': 3, 'man ki udaasi': 3, 'pichhla vishaal dukh': 3, 'nirashay': 3,
    'tanaav bharah dukh': 3, 'dard se bharah': 3, 'tanhaai': 2
}

        },

        'Stressed': {
            'stressed': 3, 'anxious': 3, 'panic': 3, 'overwhelmed': 2, 
    'nervous': 2, 'worried': 2, 'tired': 1, 'exhausted': 2, 
    'frustrated': 2, 'pressure': 2, 'tension': 2, 'irritated': 2, 
    'tense': 2, 'drained': 2, 'fatigued': 2, 'troubled': 2, 
    'overloaded': 2, 'burned out': 2, 'agitated': 2, 
    'distressed': 3, 'uneasy': 2, 'frazzled': 2, 'worried sick': 3, 
    'fearful': 2, 'distraught': 2, 'rattled': 2, 'shaken': 2, 
    'panicked': 3, 'unsettled': 2, 'restless': 2, 'harried': 2,
    # Adding more English and Hindi words
    'nervy': 2, 'uneasy': 2, 'disconcerted': 2, 'disturbed': 2,
    'tired out': 2, 'burnout': 3, 'unhinged': 3, 'besieged': 2,
    'flustered': 2, 'disquieted': 2, 'worn out': 2, 'exasperated': 2,
    'panicked': 3, 'strained': 2, 'frenzied': 2, 'jittery': 2,
    'mood swings': 3, 'drained mentally': 2, 'overloaded mentally': 2,
    # Hindi transliterations
    'chintit': 3, 'chintat': 3, 'vyathit': 3, 'pareshan': 3, 
    'tanaav': 3, 'nervous': 2, 'tired': 1, 'thaka hua': 2,
    'jhatka': 2, 'khajil': 2, 'pareshani': 2, 'tension me': 2,
    'ghabrahat': 3, 'dar': 2, 'bechain': 2, 'adhik dabav': 2,
    'chintit dil': 2, 'vyakul': 2, 'preshan': 3, 'tanaav mein': 2,
    'jhunjhuna': 2, 'khud ko thoda bhej': 2, 'peeda': 2, 
    'haath mein chinta': 2
        },

        'Happy': {
             'happy': 3, 'excited': 3, 'joyful': 3, 'wonderful': 2, 
    'good': 2, 'pleasant': 2, 'content': 2, 'cheerful': 3,
    'bright': 2, 'blessed': 2, 'optimistic': 3,
    # Adding more English and Hindi words
    'delighted': 3, 'thrilled': 3, 'grateful': 3, 'elated': 3, 
    'hopeful': 3, 'pleased': 2, 'satisfied': 2, 'blissful': 3, 
    'euphoric': 3, 'positive': 3, 'radiant': 2, 'jovial': 3,
    # Hindi transliterations
    'khush': 3, 'utsahit': 3, 'anandi': 3, 'accha': 2, 
    'sakaratmak': 3, 'muskurana': 2, 'sukhi': 2, 'mazedaar': 2, 
    'adhyatmik': 2, 'ummeed': 3, 'santusht': 2, 'prasann': 3, 
    'nirmal': 2, 'tandurust': 3, 'prashansha': 2, 'anandit': 3
        }

    }

    mood_scores = {mood: 0 for mood in mood_keywords}
    text_lower = text.lower()
    
    # Check for emergency situations
    for keyword, weight in emergency_keywords.items():
        if keyword in text_lower and not is_negated(keyword, text_lower):
            return 'Emergency'

    # Analyze the mood based on keywords
    for mood, keywords in mood_keywords.items():
        for keyword, weight in keywords.items():
            if keyword in text_lower:
                if is_negated(keyword, text_lower):
                    # If negated, reverse the mood score effect
                    if mood == 'Happy':
                        mood_scores['Depressed'] += weight
                    elif mood == 'Depressed':
                        mood_scores['Happy'] += weight
                    elif mood == 'Stressed':
                        mood_scores['Neutral'] += weight
                else:
                    mood_scores[mood] += weight
    
    # Refine with sentiment analysis
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    # Adjust mood scores based on sentiment polarity
    if sentiment_score > 0.3:
        mood_scores['Happy'] += 2
    elif sentiment_score < -0.3:
        mood_scores['Depressed'] += 2
    elif sentiment_score < 0:
        mood_scores['Stressed'] += 1

    # Determine the mood with the highest score
    max_score = max(mood_scores.values())
    if max_score == 0:
        return 'Neutral'

    dominant_mood = [mood for mood, score in mood_scores.items() if score == max_score]
    
    # If multiple moods have the same score, use sentiment as a tiebreaker
    if len(dominant_mood) > 1:
        if sentiment_score > 0.1:
            return 'Happy'
        elif sentiment_score < -0.1:
            return 'Depressed'
        else:
            return 'Neutral'
    
    return dominant_mood[0]

# # Example usage
# text_input = "It’s harder each day, but I try to stay optimistic even when I can’t find motivation."
# print(detect_mood(text_input))
