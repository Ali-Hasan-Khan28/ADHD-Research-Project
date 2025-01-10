from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key = os.environ.get('OPENAI_API_KEY'))
# Set your OpenAI API key

def estimate_task_completion_time(task_description):
    """
    Use OpenAI API to estimate how long a task might take.
    Returns the estimated time in seconds.
    """
    try:
        # Call OpenAI GPT model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in time management and task evaluation. You don't need to write a descriptive answer, just write a numeric value with no time or any other units of how many seconds will any task take?"},
                {"role": "user", "content": f"How much time (in seconds) would it take to complete this task: {task_description}?"}
            ],
        )

        # Extract the time from OpenAI's response
        predicted_time = response.choices[0].message.content
        
        # Parse the time in seconds from the response
        try:
            return int(predicted_time.strip())  # Assuming GPT returns seconds
        except ValueError:
            raise ValueError(f"Unexpected format: {predicted_time}")

    except Exception as e:
        print(f"Error: {e}")
        return 10  # Default to 10 seconds if something goes wrong
