import google.generativeai as genai
import os
from PIL import Image
import json

config_file = "config.json"  # Replace with your JSON file's name if different
if os.path.exists(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)
        GEMINI_API_KEY = config.get("GEMINI_API_KEY")
else:
    raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

## Configure the API

genai.configure(api_key=GEMINI_API_KEY)

# Sender and Theme of Phishing campaign
sender_name = "Proximus"
phishing_reason = "Annual staff party on "
fake_link = "confirm attendance"

### Load/Set the variables for the target --> this can be altered to input fields from the user (target selection, and then pull in from a database)
name = "Bas"
surname="Van Assche"
email="bas.van.assche@proximus-ada.com"
business_unit="IT"
team_name="CyberSecurity"

### Load/Set the variables for the theme --> this can be altered to input fields from the user (target selection, and then pull in from a database)
# Simulated phishing themes for security awareness training
'''grounding_text = "data/static/MS_Azure_original_email.html"
img_location = "data/static/MS_Azure.PNG" # Note, there can be several images given with the prompting, but then the code needs to change to handle this
img = Image.open(img_location)'''

prompt_body = f'''Write an email from {sender_name} to {name} {surname} in the {team_name} team on the following theme: {phishing_reason}.
            He will have to click on this link : {fake_link}. Only write the body of this email.'''
             
output_composition = "The output is an html formatted email. The email mimicks the image in the uploaded file. The output contains the logo found in the uploaded image. The logo is not retrieved from the website https://upload.wikimedia.org/wikipedia/commons.",

# Combine the grounding text and the prompt body to make the fully engineered prompt
prompt_input_text = f"Prompt:\n{prompt_body}/n---/nOutput Composition:/n{output_composition}"



# Set the AI model for img-and-text-to-phishing-email
# Here you give the model name, generation config (here you set for instance the creativity of the response via temperature) and system instruction (how the model should behave, what it should do)
model_name_phish = "gemini-2.0-flash-exp"
generation_config = {"temperature": 0.9,"top_p": 0.95,"top_k": 64,"max_output_tokens": 8192,"response_mime_type": "text/plain"}
system_instruction ="You are a HR staff member. You write emails in concise language, fluent English and with the tone of a large corporation. You are relaxed in your language because it's an informal event, but your goal is to make the employee click on a link to confirm their attendence to the annual staff party. You generate output as an email in html format. You recreate the layout of the output to mimick the uploaded image file. You search for the logo found in the uploaded image, and include a working link of the logo in the generated output.",
model = genai.GenerativeModel(model_name=model_name_phish, generation_config=generation_config, system_instruction=system_instruction)

# send everything to the Geminin to generate a response
response = model.generate_content([prompt_input_text], stream=True)
response.resolve()
print(response.text)

# Save the output to a file
with open("phishing_email.html", "w", encoding="utf8") as file:
    file.write(response.text)