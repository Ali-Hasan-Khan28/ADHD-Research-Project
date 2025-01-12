# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv(), override=True)
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# import getpass
# import os
# if 'GOOGLE_API_KEY' not in os.environ:
#     os.environ['GOOGLE_API_KEY'] = getpass.getpass('Provide your Google API Key: ')
# import google.generativeai as genai
# # for model in genai.list_models():
# #     print(model.name)
    
# # Create an instance of the LLM, using the 'gemini-pro' model with a specified creativity level

# llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.9)

# # Send a creative prompt to the LLM
# prompt = PromptTemplate.from_template('You are a content creator. Write me a tweet about {topic}')

# # Create a chain that utilizes both the LLM and the prompt template
# chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
# topic = 'Why will AI change the world'
# response = chain.invoke(input=topic)
# print(response)



from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os
import getpass
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv(find_dotenv(), override=True)

# Set your Google API key
if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Provide your Google API Key: ')

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.9)

def estimate_task_completion_time(task_description):
    """
    Use Gemini API to estimate how long a task might take.
    Returns the estimated time in seconds.
    """
    try:
        # Define the prompt for the Gemini API
        prompt = PromptTemplate.from_template(
            "You are an expert in time management and task evaluation. You don't need to write a descriptive answer, "
            "just write a numeric value with no time or any other units of how many seconds will any task take? Task: {task_description}"
        )

        # Create a chain that utilizes the LLM and the prompt template
        chain = prompt | llm  # Use the RunnableSequence syntax

        # Get the response from Gemini API
        response = chain.invoke({"task_description": task_description})
        # Parse the time in seconds from the response
        try:
            return int(response.content)  # Assuming the response is directly the numeric value
        except ValueError:
            raise ValueError(f"Unexpected format: {response}")

    except Exception as e:
        print(f"Error: {e}")
        return 10  # Default to 10 seconds if something goes wrong


# Example usage
estimated_time = estimate_task_completion_time("teeth brush and facewashing")
print(f"Estimated time: {estimated_time} seconds")
