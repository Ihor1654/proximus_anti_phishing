# Import the Python SDK
import google.generativeai as genai # type: ignore
import json
import os

# Load the JSON file
config_file = "config.json"  # Replace with your JSON file's name if different
if os.path.exists(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)
        GEMINI_API_KEY = config.get("GEMINI_API_KEY")
else:
    raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

genai.configure(api_key=GEMINI_API_KEY)

# Inititalize the generative model (Gemini)
model = genai.GenerativeModel('gemini-pro')

# Generate text for phishing email
name = "John"
surname="Doe"
email="john.doe@example.com"
business_unit="Sales"
team_name="B2B Sales"

#Create an approximate combination of phishing parameters
phishing_examples = [
    {"Reason": "Account Suspicious Activity", "Fake Link": "https://example.com/secure-login", "Created By": "Sam Sussy"},
    {"Reason": "Password Expiry Notification", "Fake Link": "https://example.com/reset-password", "Created By": "Sally Sneaky"},
    {"Reason": "Exclusive Training Webinar", "Fake Link": "https://example.com/join-webinar", "Created By": "Richard Rascal"},
    {"Reason": "Email Storage Full", "Fake Link": "https://example.com/manage-storage", "Created By": "Bernard Bandit"}
]

#Take a random reason
import random
random_pick = random.choice(phishing_examples)

#Formulate a prompt
system_instructions = "You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You write emails to customers to persuade them to click on a link. You are neutral in your language, but your goal is to make the customer click on a link to buy a product."
output_composition= "Write an email that is convincing and that will make the customer click on the link. The email should be written in a professional tone, and should be concise and to the point. Give the output as text only, without any formatting."

prompt_body=f'''Write an email from {random_pick["Created By"]} to {name} {surname} from the {team_name} team on the following theme: {random_pick["Reason"]}.
He will have to click on this link : {random_pick["Fake Link"]}. Only write the body of this email.'''

prompt_engineered=f"{system_instructions}/n---/n{prompt_body}/n---/n{output_composition}"

print("Prompt:",prompt_engineered)

# Generate text
response = model.generate_content(prompt_engineered)
print("Output:")
print(response.text)
