
from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
from deep_translator import GoogleTranslator  # ✅ new import

app = Flask(__name__)

recognizer = sr.Recognizer()

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
            # Recognize speech using Google Speech Recognition API (Hindi input)
            speech_text = recognizer.recognize_google(audio, language='hi-IN')
            print("Recognized Speech:", speech_text)
            if speech_text.lower() == "exit":
                return jsonify(transcribedText="Listening ended.")
        except sr.UnknownValueError:
            print("Could not understand.")
            return jsonify(transcribedText="Could not understand.")
        except sr.RequestError:
            print("Poor Network.")
            return jsonify(transcribedText="Poor Network.")

        # ✅ Translate the speech text to English
        try:
            translated_text = GoogleTranslator(source='auto', target='en').translate(speech_text)
            print("Translated Text:", translated_text)
        except Exception as e:
            print("Translation failed:", str(e))
            translated_text = "Translation failed."

       

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
