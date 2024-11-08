# chatbot/views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse
from lead_management.models import Lead
import requests
import logging
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)

# Ensure OpenAI API key from the environment is used
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define conversation steps
steps = [
    "customer_description",
    "ideal_customer_profile",
    "ideal_position_identification",
    "geographic_target",
    "company_list_creation",
    "lead_generation",
    "refine_criteria"
]

def home(request):
    # Render a simple template or return a basic HttpResponse
    return render(request, 'chatbot/home.html')  # Ensure you have a 'home.html' in 'chatbot/templates/chatbot'

#@login_required
@csrf_exempt
def chatbot_interaction(request):
    # Handle the user's POST request and fetch a response from ChatGPT
    if request.method == "POST":
        user_input = request.POST.get('user_input', '').strip()
        #chat_history = request.session['chat_history']

        #if user_input:
            #chat_history.append({'sender': 'user', 'message': user_input})

        try:
            # Process each step in the conversation flow
            if steps[current_step] == "customer_description":
                bot_response = "Please describe your startup. What product/service do you offer?"
                request.session['startup_description'] = user_input

            elif steps[current_step] == "ideal_customer_profile":
                bot_response = "Describe your ideal B2B customer. What industry, challenges, or needs align with what you offer?"
                request.session['ideal_customer_profile'] = user_input

            elif steps[current_step] == "ideal_position_identification":
                bot_response = chatgpt_generate_roles(user_input)
                request.session['ideal_position'] = user_input

            elif steps[current_step] == "geographic_target":
                bot_response = "Which city or region would you like to target for lead generation?"
                request.session['target_region'] = user_input

            elif steps[current_step] == "company_list_creation":
                bot_response = "Provide a list of specific companies you'd like to target or let me know if I should generate one."
                request.session['company_list'] = user_input.split(',') if user_input else []

            elif steps[current_step] == "lead_generation":
                leads_data = chatgpt_generate_roles(request.session)
                bot_response = format_leads_output(leads_data)
                current_step = -1  # End conversation after lead generation

            elif steps[current_step] == "refine_criteria":
                bot_response = "Would you like to refine your search criteria? (e.g., specify company size or industry)"
                request.session['refine_criteria'] = user_input if user_input else None

        except Exception as e:
            logger.error(f"Error during chatbot interaction: {str(e)}")
            bot_response = "An error occurred while processing your request. Please try again or adjust your input."

        #chat_history.append({'sender': 'bot', 'message': bot_response})
        current_step += 1
        request.session['current_step'] = current_step
        request.session.modified = True

        #return render(request, 'chatbot/chatbot.html', {'chat_history': request.session['chat_history']})
        chat_response = get_chatbot_response(user_input)
    return render(request, 'chatbot/chatbot.html', {"response_message": chat_response})

def chatgpt_generate_roles(description):
    prompt = f"Given the description '{description}', suggest potential decision-maker roles."
    response = get_chatbot_response(prompt)
    return response.get('choices')[0]['text'] if response else "I'm here to help! Please let me know more details."

def generate_leads(session_data):
    leads = []
    for company in session_data['company_list']:
        proxycurl_leads = proxycurl_role_lookup(company, session_data['ideal_position'], session_data['target_region'])
        for lead in proxycurl_leads:
            detailed_lead = salesql_contact_lookup(lead)
            leads.append(detailed_lead)
    return leads

def proxycurl_role_lookup(company_name, role, region):
    url = "https://nubela.co/proxycurl/api/people/role/lookup"
    headers = {"Authorization": f"Bearer {settings.PROXYCURL_API_KEY}"}
    params = {"company_name": company_name, "role": role, "region": region}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('contacts', [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Proxycurl API error: {str(e)}")
        return []

def salesql_contact_lookup(lead):
    url = "https://api.salesql.com/v2/person-search"
    headers = {"Authorization": f"Bearer {settings.SALESQL_API_KEY}"}
    params = {
        "first_name": lead['first_name'],
        "last_name": lead['last_name'],
        "company": lead['company'],
        "location": lead.get('region', '')
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        contact_data = response.json()
        return {
            "name": f"{lead['first_name']} {lead['last_name']}",
            "role": lead.get('job_title', ''),
            "company": lead['company'],
            "email": contact_data.get('email'),
            "phone": contact_data.get('phone')
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"SalesQL API error: {str(e)}")
        return {
            "name": f"{lead['first_name']} {lead['last_name']}",
            "role": lead.get('job_title', ''),
            "company": lead['company'],
            "email": None,
            "phone": None
        }

def format_leads_output(leads):
    if not leads:
        return "No leads found based on the provided criteria. Please refine your search criteria or try different options."
    
    formatted_text = "Here are the leads we found:\n"
    for lead in leads:
        contact_info = f"{lead['name']} - {lead['role']} at {lead['company']}"
        if lead.get('email'):
            contact_info += f", Email: {lead['email']}"
        if lead.get('phone'):
            contact_info += f", Phone: {lead['phone']}"
        formatted_text += contact_info + "\n"
    return formatted_text

# Helper function to fetch response from OpenAI API
def get_chatbot_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            max_tokens=100,
            messages=[
                {"role": "system", "content": "You are an assistant helping startups connect with decision-makers in companies."},
                {"role": "user", "content": message},
                {"role": "assistant", "content": (
                    "Could you confirm the ideal contact titles for your product? Common roles include "
                    "'IT Director', 'Procurement Manager', 'Operations Head', etc. "
                    "Please provide a list of companies you'd like to target, or I can suggest some based "
                    "on your industry and region. Would you prefer specific company sizes as well?"
                )}
            ]
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"Error fetching response: {str(e)}"