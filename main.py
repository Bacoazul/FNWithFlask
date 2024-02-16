from flask import Flask, render_template, request, jsonify, session
from num2words import num2words
from gtts import gTTS
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for the session


# Convert a number to French words
def number_to_french_words(number):
  return num2words(number, lang='fr')


@app.route('/', methods=['GET'])
def display_random_number():
  session['random_num'] = random.randint(1, 100)
  tts = gTTS(text=number_to_french_words(session.get('random_num')), lang='fr')
  audio_file_path = "static/translated_number.mp3"
  tts.save(audio_file_path)
  return render_template('random_number.html')


@app.route('/refresh', methods=['GET'])
def refresh_number():
  session['random_num'] = random.randint(1, 100)
  tts = gTTS(text=number_to_french_words(session.get('random_num')), lang='fr')
  audio_file_path = "static/translated_number.mp3"
  tts.save(audio_file_path)
  return jsonify(result="Refreshed")


@app.route('/reveal', methods=['GET'])
def reveal_number():
  random_num = session.get('random_num')
  translated_num = number_to_french_words(session.get('random_num'))
  return jsonify(translated_num=translated_num, number=random_num)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
