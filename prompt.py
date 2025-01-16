import google.generativeai as genai
# pip install -q -U google-generativeai

from PIL import Image
# pip install -q -U pillow

class PromptEngineer:
    def __init__(self, phishing_theme):
        self.phishing_theme = phishing_theme

    def generate_prompt_input_text(self, name, surname, email, business_unit, team_name):
        """This function generates the prompt for the phishing email, including instructions for the output composition.
        Args: pulled in from database or user input"""
        self.name = name
        self.surname = surname
        self.email = email
        self.business_unit = business_unit
        self.team_name = team_name

        prompt_body = f'''Write an email from {self.phishing_theme["Created By"]} to {self.name} {self.surname} from the {self.team_name} team on the following theme: {self.phishing_theme["Reason"]}.
            He will have to click on this link : {self.phishing_theme["Fake Link"]}. Only write the body of this email.'''
        
        prompt_input_text=f"Grounding Text:/n---/n{self.phishing_theme["Grounding Text"]}/n---/nPrompt:/n---/n{prompt_body}/n---/nOutput Compositiont:/n---/n{self.phishing_theme["Output Composition"]}"
        
        return prompt_input_text