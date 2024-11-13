import streamlit as st
import time
from pygame import mixer

# Initialize pygame mixer for buzzer sound
mixer.init()

# Function to play buzzer sound
def play_buzzer():
    buzzer_file = 'buzzer.mp3'  # Path to your buzzer sound file
    mixer.music.load(buzzer_file)
    mixer.music.play()

# Function to play the buzzer sound 5 times consecutively
def play_buzzer_5_times():
    for i in range(5):
        play_buzzer()
        time.sleep(4)  # Short pause between buzzers

# Function to display tasks as checkboxes
def display_tasks(tasks):
    for task in tasks:
        st.checkbox(task)

# Title of the app
st.title("Daily Task Tracker with Circular Countdown and Buzzer")

# Session state to store tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Input to add tasks
new_task = st.text_input("Add a new task for today:")

if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        st.experimental_rerun()  # Rerun the app to display the new task

# Display existing tasks as checkboxes
if st.session_state.tasks:
    st.write("Your tasks for today:")
    display_tasks(st.session_state.tasks)

# Function for circular countdown timer (progress bar)
def circular_countdown(total_seconds):
    #progress_bar = st.empty()  # Create an empty container to hold the progress bar
    countdown_text = st.empty()  # Create an empty container to hold the time left text
    for i in range(total_seconds):
        remaining_time = total_seconds - i
        # Calculate the percentage of time left
        #progress = (i + 1) / total_seconds
        # Display a progress bar and countdown in MM:SS format
        mins, secs = divmod(remaining_time, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        
        # Replace the previous countdown with the new one in the same place
        countdown_text.markdown(f"<h2 style='text-align: center;'>Time left: {timer}</h2>", unsafe_allow_html=True)
        #progress_bar.progress(progress)  # Update the progress bar
        time.sleep(1)  # Wait for 1 second before updating

# Start the buzzer and countdown timer
st.write("Click 'Start Buzzer' to begin the countdown with a circular progress bar (2 minutes).")
if st.button("Start Buzzer"):
    while True:
        # Countdown for 2 minutes (120 seconds)
        circular_countdown(10)
        
        # Play the buzzer 5 times consecutively
        #st.write("Playing buzzer 5 times...")
        play_buzzer_5_times()
        
        # Restart the countdown after the buzzer has played 5 times
        #st.write("Buzzer sound played 5 times! Countdown will restart.")
