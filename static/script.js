// Select elements
const startButton = document.getElementById('startButton');
const saveTextButton = document.getElementById('saveTextButton');
const loadingSpinner = document.getElementById('loadingSpinner');
const transcribedTextElement = document.getElementById('transcribedText');
const translatedTextElement = document.getElementById('translatedText');

// Add event listener to start button
startButton.addEventListener('click', () => {
    // Show loading spinner
    loadingSpinner.style.display = 'block';

    // Disable start button and enable stop button
    startButton.disabled = true;

    // Call Flask endpoint to start listening
    fetch('/start-listening')
        .then(response => response.json())
        .then(data => {
            // Update UI with transcribed and translated text
            transcribedTextElement.textContent = data.speechText;
            translatedTextElement.textContent = data.translatedText;

            // Hide loading spinner
            loadingSpinner.style.display = 'none';

            // Enable start button and disable stop button
            startButton.disabled = false;
        })
        .catch(error => {
            // Handle any errors
            console.error("An error occurred:", error);
            loadingSpinner.style.display = 'none';
            startButton.disabled = false;
        });
});

// Add event listener to save text button
saveTextButton.addEventListener('click', () => {
    // Get speech and translated text from UI
    const speechText = transcribedTextElement.textContent;
    const translatedText = translatedTextElement.textContent;

    // Make a POST request to save text
    fetch('/save-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ speechText, translatedText })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error("An error occurred:", error);
    });
});
