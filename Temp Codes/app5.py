import streamlit as st
import time
from pygame import mixer
from datetime import datetime, timedelta

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

# Session state to store tasks and timer-related info
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

# Input to add tasks
new_task = st.text_input("Add a new task for today:")

if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        new_task = ""  # Clear the input field

# Display existing tasks as checkboxes
if st.session_state.tasks:
    st.write("Your tasks for today:")
    display_tasks(st.session_state.tasks)

# Function for circular countdown timer
def circular_countdown():
    now = datetime.now()
    end_time = st.session_state.timer_start + timedelta(seconds=10)
    remaining_time = (end_time - now).total_seconds()
    
    if remaining_time > 0:
        mins, secs = divmod(int(remaining_time), 60)
        timer_text = '{:02d}:{:02d}'.format(mins, secs)
        return timer_text, False  # Timer is still running
    else:
        return "00:00", True  # Timer finished

# Start the buzzer and countdown timer
st.write("Click 'Start Buzzer' to begin the timer")

if st.button("Start Buzzer"):
    if not st.session_state.timer_running:
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_running = True

# Timer display
if st.session_state.timer_running:
    countdown_placeholder = st.empty()  # Create a placeholder for the countdown

    # Continuously update the countdown without rerunning the whole script
    while True:
        timer_text, timer_finished = circular_countdown()
        
        countdown_placeholder.markdown(f"<h2 style='text-align: center;'>Time left: {timer_text}</h2>", unsafe_allow_html=True)
        
        if timer_finished:
            st.session_state.timer_running = False
            play_buzzer_5_times()
            
            # Automatically restart the timer for the next 2-minute cycle
            st.session_state.timer_start = datetime.now()
            st.session_state.timer_running = True
        
        time.sleep(1)  # Update the countdown every second
