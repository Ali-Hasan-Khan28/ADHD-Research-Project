import time
import streamlit as st

def play_buzzer():
    buzzer_html = """
    <audio id="buzzer_audio" autoplay>
        <source src="https://dl.dropbox.com/scl/fi/xo9qjc0i8tll097eh8vo9/buzzer.mp3?rlkey=tv0gj6jkz9ljrytqmiodfslkx&st=eahbmt3y&" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    <script>
        var buzzer = document.getElementById('buzzer_audio');
        buzzer.onended = function() {
            buzzer.currentTime = 0;  // Reset the audio to start
        };
    </script>
    """
    st.markdown(buzzer_html, unsafe_allow_html=True)
    #time.sleep(6)  # Short pause to ensure the browser has time to process the audio

# Example usage
for _ in range(5):  # Play buzzer 5 times
    play_buzzer()
    time.sleep(5)  # Delay to prevent overlap
