from gemini_functions import GeminiPhish # custom class and function
from prompt import PromptEngineer # custom class and function

from dotenv import load_dotenv

from PIL import Image

# https://ai.google.dev/tutorials/python_quickstart

load_dotenv()

### Load/Set the variables for the target --> this can be altered to input fields from the user (target selection, and then pull in from a database)
name = "Bas"
surname="Van Assche"
email="bas.van.assche@proximus-ada.com"
business_unit="IT"
team_name="CyberSecurity"

### Load/Set the variables for the theme --> this can be altered to input fields from the user (target selection, and then pull in from a database)
# Simulated phishing themes for security awareness training
phishing_themes = [
    {"Reason": "Take action to keep your Azure free account and services active", 
     "Landing Page": "https://portal.azure.com/", 
     "Created By": "Bernard Bandit",    
     "System Instructions":
        "You are a professional email campaign expert. You write emails in concise language, fluent English and with the tone of a large corporation. You are neutral in your language, but your goal is to make the customer click on a link to buy a product. You generate output as an email in html format. You recreate the layout of the output to mimick the uploaded image file. You search for the logo found in the uploaded image, and include a working link of the logo in the generated output. You replace the subscription ID in the image with a random subscriptionID in the same format.",
     "Example Image":"MS_Azure.PNG",
     "Output Composition":
        "The output is an html formatted email. The email mimicks the image in the uploaded file. The output contains the logo found in the uploaded image. The logo is not retrieved from the website https://upload.wikimedia.org/wikipedia/commons.",
    "Grounding Text":"MS_Azure_original_email.html",
    "Generation Config": {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }
    }
]

# Randomly select a phishing theme for the simulation
phishing_theme = phishing_themes[0]
generation_config = phishing_theme["Generation Config"]
system_instruction = phishing_theme["System Instructions"]

# Initiate instance of PromptEngineer class
promptengineer = PromptEngineer(phishing_theme)

# Set the AI model for img-and-text-to-phishing-email
model_name_phish = "gemini-2.0-flash-exp"
phishing_ai = GeminiPhish(model_name_phish, generation_config, system_instruction)

def phish_response(input, img):
    return phishing_ai.generate_response(input_text=input, input_img=img)

if __name__ == "__main__":

    # prompt and image to phishing email

    prompt = promptengineer.generate_prompt_input_text(name, surname, email, business_unit, team_name)
    print("Prompt generated in Python: ", prompt)
    img = phishing_theme["Example Image"]
    print(phish_response(input=prompt, img=img))    


