# Import the Python SDK
import google.generativeai as genai # type: ignore
import json
import os


# Select a theme for the phishing campaign to create an approximate combination of phishing parameters
phishing_themes = [
    {
        "Reason": "Account Suspicious Activity", 
        "Fake Link": "https://example.com/secure-login", 
        "Created By": "Sam Sussy", 
        "System Instructions":"You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product.",
     "Output composition":"Write an email that is convincing and that will make the customer click on the link. The email should be written in a professional tone, and should be concise and to the point. Give the output as text only, without any formatting.",
     "generation_config": {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }},  
    {"Reason": "Password Expiry Notification", 
     "Fake Link": "https://example.com/reset-password", 
     "Created By": "Sally Sneaky",    
     "System Instructions":"You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product.",
     "Output composition":"Write an email that is convincing and that will make the customer click on the link. The email should be written in a professional tone, and should be concise and to the point. Give the output as text only, without any formatting.",
     "generation_config": {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }},
    {"Reason": "Exclusive Training Webinar", 
     "Fake Link": "https://example.com/join-webinar", 
     "Created By": "Richard Rascal",    
     "System Instructions":"You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product.",
     "Output composition":"Write an email that is convincing and that will make the customer click on the link. The email should be written in a professional tone, and should be concise and to the point. Give the output as text only, without any formatting.",
     "generation_config": {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }},
    {"Reason": "Email Storage Full", 
     "Fake Link": "https://example.com/manage-storage", 
     "Created By": "Bernard Bandit",    
     "System Instructions":"You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product.",
     "Output composition":"Write an email that is convincing and that will make the customer click on the link. The email should be written in a professional tone, and should be concise and to the point. Give the output as text only, without any formatting.",
     "generation_config": {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }}
]

#Take a random reason --> this can be modified to input fields from the user (selecting target, theme, etc.)
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

# Create the model using the configuration settings that fit with the campaign and the phishing theme

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=random_pick["generation_config"],
  system_instruction=random_pick["system_instructions"])

# Generate text for phishing email
## Define the variables for the email --> this can be altered to input fields from the user (target selection, and then pull in from a database)
name = "John"
surname="Doe"
email="john.doe@example.com"
business_unit="Sales"
team_name="B2B Sales"

#Formulate a prompt
"""
I commented this out for now, because it should come from the phishing themes list above.
system_instructions = "You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product."
output_composition= "Write an email that is convincing and that will make the customer click on the link. The email should be written in a professional tone, and should be concise and to the point. Give the output as text only, without any formatting."
"""
prompt_body=f'''Write an email from {random_pick["Created By"]} to {name} {surname} from the {team_name} team on the following theme: {random_pick["Reason"]}.
He will have to click on this link : {random_pick["Fake Link"]}. Only write the body of this email.'''

prompt_engineered=f"{prompt_body}/n---/n{random_pick["Output composition"]}"

print("Engineered prompt:",prompt_engineered)

# Generate text
response = model.generate_content(prompt_engineered)
print("Gemini Output:")
print(response.text)
