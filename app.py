from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
from google_trans_new import google_translator

app = Flask(__name__)

# Create a recognizer and translator instance
recognizer = sr.Recognizer()
translator = google_translator()

@app.route('/')
def index():
    # Render the index.html file
    return render_template('index.html')

@app.route('/start-listening')
def start_listening():
    
    with sr.Microphone() as source:
        print("Speak now!")
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Speech Recognition API
            speech_text = recognizer.recognize_google(audio, language='hi-IN')
            print(speech_text)
            if speech_text == "exit":
                return jsonify(transcribedText="Listening ended.")
        except sr.UnknownValueError:
            print("Could not understand.")
            return jsonify(transcribedText="Could not understand.")
        except sr.RequestError:
            print("Poor Network.")
            return jsonify(transcribedText="Poor Network.")
        
        # Translate the speech text to English
        translated_text = translator.translate(speech_text, lang_tgt='en')
        print(translated_text)

        # Save speech and translated text to a file
        save_text_to_file(speech_text, translated_text)

        # Return both speech text and translated text as JSON
        return jsonify({
            'speechText': speech_text,
            'translatedText': translated_text
        })

@app.route('/save-text', methods=['POST'])
def save_text():
    data = request.get_json()
    speech_text = data['speechText']
    translated_text = data['translatedText']

    # Save text to a file
    save_text_to_file(speech_text, translated_text)
    
    return jsonify(message="Text saved successfully!")

def save_text_to_file(speech_text, translated_text):
    with open('speech_translation.txt', 'a', encoding='utf-8') as file:
        file.write(f"Speech Text (Hindi): {speech_text}\n")
        file.write(f"Translated Text (English): {translated_text}\n")
        file.write("\n")  # Adding a line break between entries

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
