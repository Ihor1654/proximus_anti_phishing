# Import the Python SDK

import json
import os
import PIL.Image
from dotenv import load_dotenv
import google.generativeai as genai # type: ignore

load_dotenv()

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Simulated phishing themes for security awareness training
phishing_themes = [
    
    {"Reason": "Email Storage Full", 
     "Fake Link": "https://example.com/manage-storage", 
     "Created By": "Bernard Bandit",    
     "System Instructions":
        "You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product.",
     "Example":"",
     "Output Composition":
        "The output is an email, in html based on the example above.",
        "Generation Config": {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }}
]
"""commented out option for phishing theme so it is easier to test at the moment
        {
        "Reason": "Account Suspicious Activity", 
        "Fake Link": "https://example.com/secure-login", 
        "Created By": "Simulated Phishing Exercise", 
        "System Instructions": (
            "This email is part of a simulated phishing exercise for security awareness training. "
            "The email mimics a phishing attempt to educate users on identifying and avoiding phishing emails. "
            "Always verify the sender and the legitimacy of links before clicking."
        ),
        "Output Composition": (
            "Write a simulated phishing email for training purposes. "
            "The email should mimic a professional tone but contain typical red flags of phishing emails, "
            "such as urgency, vague greetings, or requests to click suspicious links. Clearly label the email as a simulation."
        ),
        "Generation Config": {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain"
        }"""
# Randomly select a phishing theme for the simulation
import random
random_pick = random.choice(phishing_themes)

# Configure the API connection
## Load the JSON file
config_file = "config.json"  # Replace with your JSON file's name if different
if os.path.exists(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)
        GEMINI_API_KEY = config.get("GEMINI_API_KEY")
else:
    raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

## Configure the API
#genai.configure(api_key=os.environ["GEMINI_API_KEY"])
genai.configure(api_key=GEMINI_API_KEY)

#import the image
img=PIL.Image.open("microsoft_email_example.png")   #replace with the image you want to use    

# Create the model using the configuration settings that fit with the campaign and the phishing theme

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
,



#Formulate a prompt
example_email = open(file="microsoft_email_example.txt", encoding="utf8").read().strip()

# Generate text for phishing email
## Define the variables for the email --> this can be altered to input fields from the user (target selection, and then pull in from a database)
name = "Bas"
surname="Van Assche"
email="bas.van.assche@proximus-ada.com"
business_unit="IT"
team_name="CyberSecurity"
phishing_theme=random_pick
generation_config=random_pick["Generation Config"],
system_instruction=random_pick["System Instructions"]

def prompt_input_text(name, surname, email, business_unit, team_name, phishing_theme):
    """This function generates the prompt for the phishing email, including instructions for the output composition.
    Args: pulled in from database or user input"""

    prompt_body = f'''Write an email from {phishing_theme["Created By"]} to {name} {surname} from the {team_name} team on the following theme: {phishing_theme["Reason"]}.
        He will have to click on this link : {phishing_theme["Fake Link"]}. Only write the body of this email.'''
    
    prompt_input_text=f"{prompt_body}/n---/n{phishing_theme["Output Composition"]}"
    
    return prompt_input_text

print("Engineered prompt:",prompt_input_text)

# Generate text
response = model.generate_content(prompt_input_text)
print("Gemini Output:")
print(response.text)

# Save the output to a file
with open("phishing_email.html", "w", encoding="utf8") as file:
    file.write(response.text)
