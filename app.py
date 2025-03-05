import streamlit as st
import time
from datetime import datetime, timedelta
from task_evaluator import estimate_task_completion_time  # Import the new function #openai API Code
# from gemini import estimate_task_completion_time
# Function to play buzzer sound 5 times consecutively using HTML5 audio tag
def play_buzzer_5_times():
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
    time.sleep(6)  # Short pause between buzzers to avoid overlap

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

        # Estimate task completion time using OpenAI
        estimated_seconds = estimate_task_completion_time(new_task)
        print(estimated_seconds)

        st.session_state.task_timers[task_id] = {
            'timer_start': None,
            'timer_end': None,
            'timer_running': False,
            'timer_complete': False,
            'remaining_time_display': f"{estimated_seconds} sec",
            'estimated_seconds': estimated_seconds  # Store estimated time
        }
        st.session_state.force_rerun = not st.session_state.force_rerun  # Toggle to force rerun

# Function to update countdown timers
def update_task_timers():
    for task_id, timer in st.session_state.task_timers.items():
        print(task_id,timer)
        if timer['timer_running'] and not timer['timer_complete']:
            remaining_time = (timer['timer_end'] - datetime.now()).total_seconds()
            if remaining_time <= 0:
                # When the timer reaches zero
                timer['timer_running'] = False
                timer['timer_complete'] = True
                print("Hello are you listening")
                play_buzzer_5_times()  # Play buzzer for task
                timer['remaining_time_display'] = "Complete"
            else:
                # Display remaining time in format 00:XX
                minutes, seconds = divmod(int(remaining_time), 60)
                timer['remaining_time_display'] = f"{minutes:02}:{seconds:02}"
        elif not timer['timer_running']:
            # Display estimated time when not running
            timer['remaining_time_display'] = f"{timer['estimated_seconds']} sec"

# Display tasks with individual start buttons and timers
if st.session_state.tasks:
    st.write("Your tasks for today:")
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.checkbox(task, key=f"task_{i}")
        with col2:
            if st.button("Start Timer", key=f"start_timer_{i}"):
                # Set the start and end time based on OpenAI's estimate
                estimated_seconds = st.session_state.task_timers[i]['estimated_seconds']
                st.session_state.task_timers[i]['timer_start'] = datetime.now()
                st.session_state.task_timers[i]['timer_end'] = datetime.now() + timedelta(seconds=estimated_seconds)
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
st.write("Click 'Start Timer' next to each task to begin the countdown timer. "
         "The duration is predicted by AI based on your task description.")
