// Use the variables
var number = window.number;
var translatedNum = window.translatedNum;

document.querySelector('audio').addEventListener('play', function() {
  document.getElementById('numberInput').focus();
});

function refreshNumber(url) {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      document.getElementById('audioSource').src = window.audioSourceUrl + "?cb=" + Date.now();
      document.querySelector('audio').load();
      document.getElementById('numberInput').value = '';  // Clear the input box
      document.getElementById('message').textContent = '';  // Clear the message
      number = data.number;
      translatedNum = data.translated_num;
    });
}

function revealNumber() {
  document.getElementById('message').textContent = 'The number was ' + number + ', which is ' + translatedNum + ' in French.';
}

function compareNumber() {
  var userNumber = document.getElementById('numberInput').value;
  var messageElement = document.getElementById('message');
  var audioElement = new Audio(window.correctGuessUrl); 
    audioElement.volume = 0.2; // 50% volume
  messageElement.classList.remove('animate__animated','animate__bounceIn');
  void messageElement.offsetWidth;
  if (userNumber == number) {
    messageElement.textContent = 'Congratulations! You guessed the number correctly.';
    messageElement.className = 'animate__animated animate__bounceIn';
    audioElement.play(); // Play the audio
  } else {
    messageElement.textContent = 'That\'s not correct, but don\'t give up! Try again!';
  }
}

