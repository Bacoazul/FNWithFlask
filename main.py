from flask import Flask, render_template, request, jsonify, session
from num2words import num2words
from gtts import gTTS
import random
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for the session


# Convert a number to French words
def number_to_french_words(number):
  return num2words(number, lang='fr')


@app.route('/', methods=['GET', 'POST'])
def display_random_number():
  message = ''

  if request.method == 'POST':
    user_guess = int(request.form['guess'])
    if user_guess == session.get('random_num'):
      message = "Congratulations! You guessed the number correctly."
      translated_num = number_to_french_words(session.get('random_num'))
      return jsonify(result=message, translated_num=translated_num)
    else:
      message = "That's not correct, but don't give up! Try again!"
      return jsonify(result=message)

  session['random_num'] = random.randint(1, 100)
  tts = gTTS(text=number_to_french_words(session.get('random_num')), lang='fr')
  audio_file_path = "static/translated_number.mp3"
  tts.save(audio_file_path)
  cache_buster = time.time()

  return render_template('random_number.html',
                         cache_buster=cache_buster,
                         message=message)


@app.route('/guess', methods=['POST'])
def guess_number():
  user_guess = int(request.form['guess'])
  if user_guess == session.get('random_num'):
    session.pop('random_num', None)  # Clear the session
    return jsonify(result="Congratulations! You guessed the number correctly.")
  else:
    return jsonify(result="That's not correct, but don't give up! Try again!")



@app.route('/reveal', methods=['GET'])
def reveal_number():
  random_num = session.get('random_num')
  translated_num = number_to_french_words(session.get('random_num'))
  #return jsonify(translated_num=translated_num)
  return jsonify(translated_num=translated_num, number=random_num)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
