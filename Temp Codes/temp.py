import streamlit as st
import time
from pygame import mixer
from datetime import datetime, timedelta

# Initialize pygame mixer for buzzer sound
mixer.init()
buzzer_file = 'assets/buzzer.mp3'  # Path to your buzzer sound file
mixer.music.load(buzzer_file)  # Preload the buzzer sound

# Function to play buzzer sound 5 times consecutively
def play_buzzer_5_times():
    # for _ in range(5):
    mixer.music.play()
    time.sleep(3)  # Short pause between buzzers to avoid overlap

# Title of the app
st.title("Task Tracker with Individual Timers and Buzzer")

# Session state to store tasks and timer-related info
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'task_timers' not in st.session_state:
    st.session_state.task_timers = {}
if 'force_rerun' not in st.session_state:  # Dummy variable for rerun
    st.session_state.force_rerun = False

# Input to add tasks (separate from timer logic)
new_task = st.text_input("Add a new task for today:")
add_task_button = st.button("Add Task")

if add_task_button:
    if new_task:
        task_id = len(st.session_state.tasks)  # Unique ID for each task
        st.session_state.tasks.append(new_task)
        st.session_state.task_timers[task_id] = {
            'timer_start': None,
            'timer_end': None,
            'timer_running': False,
            'timer_complete': False,
            'remaining_time_display': "00:10"
        }
        st.session_state.force_rerun = not st.session_state.force_rerun  # Toggle to force rerun

# Function to update countdown timers
def update_task_timers():
    for task_id, timer in st.session_state.task_timers.items():
        if timer['timer_running'] and not timer['timer_complete']:
            remaining_time = (timer['timer_end'] - datetime.now()).total_seconds()
            if remaining_time <= 0:
                # When the timer reaches zero
                timer['timer_running'] = False
                timer['timer_complete'] = True
                play_buzzer_5_times()  # Play buzzer for task
                timer['remaining_time_display'] = "Complete"
            else:
                # Display remaining time in format 00:XX
                minutes, seconds = divmod(int(remaining_time), 60)
                timer['remaining_time_display'] = f"{minutes:02}:{seconds:02}"
        elif not timer['timer_running']:
            # If timer is not running, keep the default display
            timer['remaining_time_display'] = "00:10"

# Display tasks with individual start buttons and timers
if st.session_state.tasks:
    st.write("Your tasks for today:")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.checkbox(task, key=f"task_{i}")
        with col2:
            if st.button("Start Timer", key=f"start_timer_{i}"):
                # Set the start and end time for a 3-second countdown
                st.session_state.task_timers[i]['timer_start'] = datetime.now()
                st.session_state.task_timers[i]['timer_end'] = datetime.now() + timedelta(seconds=10)
                st.session_state.task_timers[i]['timer_running'] = True
                st.session_state.task_timers[i]['timer_complete'] = False
                st.session_state.force_rerun = not st.session_state.force_rerun  # Toggle to force rerun
        with col3:
            # Display the countdown timer
            st.write(st.session_state.task_timers[i]['remaining_time_display'])

# Continuously update countdown timers in the session state
update_task_timers()

# Add a short pause for smooth updates and rerun the app
time.sleep(1)
st.rerun()

# Explanation for the user
st.write("Click 'Start Timer' next to each task to begin a 3-second countdown timer. "
         "Once the timer completes, the buzzer will play for that task.")
