from flask import Flask, render_template, request, jsonify
from num2words import num2words
from gtts import gTTS
import random
import time

app = Flask(__name__)


# Convert a number to French words
def number_to_french_words(number):
  return num2words(number, lang='fr')


@app.route('/', methods=['GET', 'POST'])
def display_random_number():
  message = ''
  global random_num  # Make random_num a global variable so it can be accessed in the /guess route

  if request.method == 'POST':
    user_guess = int(
        request.form['guess'])  # Get the number the user guessed from the form
    if user_guess == random_num:
      message = "Congratulations! You guessed the number correctly."
      translated_num = number_to_french_words(
          random_num)  # Only translate the number if the guess is correct
      return jsonify(result=message, translated_num=translated_num)
    else:
      message = "That's not correct, but don't give up! Try again!"
      return jsonify(result=message)

  random_num = random.randint(
      1, 100)  # Generate a random number between 1 and 100
  tts = gTTS(text=number_to_french_words(random_num), lang='fr')
  audio_file_path = "static/translated_number.mp3"
  tts.save(audio_file_path)  # Save audio to a file
  cache_buster = time.time()  # Current time as a unique value

  return render_template('random_number.html',
                         cache_buster=cache_buster,
                         message=message)


@app.route('/guess', methods=['POST'])
def guess_number():
  user_guess = int(
      request.form['guess'])  # Get the number the user guessed from the form
  if user_guess == random_num:
    return jsonify(result="Congratulations! You guessed the number correctly.")
  else:
    return jsonify(result="That's not correct, but don't give up! Try again!")

@app.route('/reveal', methods=['GET'])
def reveal_number():
  translated_num = number_to_french_words(random_num)
  return jsonify(translated_num=translated_num)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
