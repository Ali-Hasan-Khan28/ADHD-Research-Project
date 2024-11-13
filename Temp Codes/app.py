import streamlit as st
import time
from pygame import mixer

# Initialize pygame mixer
mixer.init()

# Function to play buzzer sound
def play_buzzer():
    buzzer_file = 'buzzer.mp3'  # Path to the buzzer sound file
    mixer.music.load(buzzer_file)
    mixer.music.play()

# Function to display tasks as checkboxes
def display_tasks(tasks):
    for task in tasks:
        st.checkbox(task)

# Title of the app
st.title("Daily Task Tracker with Buzzer")

# Input tasks
tasks = st.text_area("Enter your daily tasks (one per line):", height=200)

# Split tasks into a list
task_list = tasks.split("\n") if tasks else []

if st.button("Start Buzzer"):
    while True:
        # Play buzzer every 2 minutes
        play_buzzer()
        time.sleep(10)  # 120 seconds = 2 minutes

# Display tasks as checkboxes
if task_list:
    st.write("Your tasks for today:")
    display_tasks(task_list)

# Stop the buzzer when checkbox is checked
if st.button("Stop Buzzer"):
    mixer.music.stop()
