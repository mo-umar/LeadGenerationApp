# chatbot/views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse
from lead_management.models import Lead
import requests
import logging
import os

# Set up logging
logger = logging.getLogger('chatbot')

# Load the API key from the environment
openai.api_key = os.getenv('OPENAI_API_KEY')
'''
def generate_linkedin_search_query(target_market, role, criteria):
    """
    Generates a LinkedIn search query based on user inputs using OpenAI's ChatCompletion API.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that creates LinkedIn search queries."},
        {"role": "user", "content": f"Generate a LinkedIn search query for {role} in the {target_market} industry with criteria: {criteria}."}
    ]
    
    # Use ChatCompletion API with gpt-3.5-turbo or gpt-4 model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can also specify "gpt-4" if you have access
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )
    
    # Extract generated content from the response
    return response.choices[0].message['content'].strip()
'''
def generate_linkedin_search_query():
    #response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",  # Choose the appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": "What is the desired role or position?"},
            {"role": "assistant", "content": "Do you have any specific criteria (e.g., company size, sector focus)?"},   
            {"role": "user", "content": "Write your specific prompt or query here."}
        ]
    

        response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    # Extract the response content
    #generated_text = response['choices'][0]['message']['content']
    #return generated_text
        return response.choices[0].message['content']

# Define the home view
def home(request):
    return render(request, 'chatbot/home.html')  # Ensure you have a 'home.html' template in 'chatbot/templates/chatbot'

'''def chatbot_interaction(request):
    """
    Handles user interaction through the chatbot, guiding users through questions
    and generating a LinkedIn search query based on their responses.
    """
    session = request.session
    if "step" not in session:
        session["step"] = 1
        session["target_market"] = ""
        session["role"] = ""
        session["criteria"] = ""
        session.save()

    if request.method == "POST":
        user_input = request.POST.get("user_input")

        # Step-by-step interaction logic
        if session["step"] == 1:
            session["target_market"] = user_input
            session["step"] = 2
            session.save()
            return JsonResponse({"bot_reply": "What is the desired role or position?"})

        elif session["step"] == 2:
            session["role"] = user_input
            session["step"] = 3
            session.save()
            return JsonResponse({"bot_reply": "Do you have any specific criteria (e.g., company size, sector focus)?"})

        elif session["step"] == 3:
            session["criteria"] = user_input
            search_query = generate_linkedin_search_query(
                #session["target_market"],
                #session["role"],
                #session["criteria"]
            )
            session["search_query"] = search_query
            session["step"] = 4
            session.save()
            return JsonResponse({
                "bot_reply": f"Here is the generated LinkedIn search query: '{search_query}'. "
                             "You can edit this query or confirm to proceed.",
                "query": search_query
            })

        elif session["step"] == 4:
            if user_input.lower() == "confirm":
                session["step"] = 5
                session.save()
                # Placeholder for LinkedIn API and SalesQL integration
                return JsonResponse({"bot_reply": "Thank you! Proceeding with LinkedIn search."})
            else:
                session["search_query"] = user_input
                session["step"] = 5
                session.save()
                return JsonResponse({
                    "bot_reply": "Your query has been updated. Proceeding with LinkedIn search.",
                    "query": user_input
                })

    return render(request, "chatbot/chatbot.html")
'''
def chatbot_interaction(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        messages = [
            {"role": "system", "content": "You are a helpful assistant for finding LinkedIn profiles."},
            {"role": "user", "content": user_input}
        ]

        # Add the next question based on current user input
        if "role" not in user_input:
            messages.append({"role": "assistant", "content": "What is the desired role or position?"})
        elif "criteria" not in user_input:
            messages.append({"role": "assistant", "content": "Do you have any specific criteria (e.g., company size, sector focus)?"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message['content']
        return render(request, "chatbot/chatbot.html", {"response": answer})
    return render(request, "chatbot/chatbot.html")

def search_linkedin_profiles(search_query):
    """
    Placeholder for LinkedIn API integration. Implement LinkedIn API or scraping logic here.
    """
    try:
        profiles = []  # Placeholder for LinkedIn API call or scraping
        # LinkedIn API integration or scraping code goes here, if allowed by TOS
        return profiles
    except requests.exceptions.RequestException as e:
        raise Exception("Network error while searching LinkedIn")

def enrich_data_with_salesql(profiles):
    """
    Placeholder for SalesQL API integration to enrich LinkedIn profiles with contact information.
    """
    try:
        enriched_data = []  # Placeholder for SalesQL API call
        # Implement SalesQL API integration here
        return enriched_data
    except requests.exceptions.RequestException as e:
        raise Exception("Network error while enriching data")
