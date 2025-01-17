import google.generativeai as genai
import os
from PIL import Image
import db_worker as db
from dotenv import load_dotenv
load_dotenv()


class TemplateCreator:
    def __init__(self,theme_id,user_id):
        self.prompt_engineer= None
        self.db_worker = db.DBWorker()
        self.gemeni_phish = None
        self.prompt = None
        self.theme = self.db_worker.get_record(db.Theme,id=theme_id)
        self.user= self.db_worker.get_record(db.User,id=user_id)
        self.config = self.db_worker.get_record(db.GenerativeConfig,id = self.theme.config_id)
        self.template = None

    def generate_prompt(self):
        self.prompt_engineer = PromptEngineer(self.theme)
        self.prompt = self.prompt_engineer.generate_prompt_input_text(name=self.user.firstname,surname=self.user.lastname,email=self.user.email,business_unit=self.user.business_unit,team_name=self.user.team)
    

    def generate_template(self):
        self.gemeni_phish = GeminiPhish(self.config,self.theme.system_instruction)
        img = os.getenv("IMG")
        self.template = self.gemeni_phish.generate_response(input_text=self.prompt,input_img=img)

    def save_tamplate_to_db(self):
        self.db_worker.add_record(db.Template,html_template=self.template,user_id=self.user.id)




    
        




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

        prompt_body = f'''Write an email from {os.getenv('FAKE_SENDER')} to {self.name} {self.surname} from the {self.team_name} team on the following theme: {self.phishing_theme.subject}.
            He will have to click on this link : {self.phishing_theme.landing_page}. Only write the body of this email.'''
        
        prompt_input_text=f"Grounding Text:/n---/n{os.getenv('GROUND_TEXT')}/n---/nPrompt:/n---/n{prompt_body}/n---/nOutput Compositiont:/n---/n{self.phishing_theme.structur_instruction}"
        
        return prompt_input_text
    

class GeminiPhish:
    def __init__(self,generation_config, system_instruction):
        self.model_name = os.getenv('MODEL_NAME')
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.generation_config = generation_config
        self.system_instruction = system_instruction
        self.config_dict = {
                            "temperature": self.generation_config.temperature,
                            "top_p": self.generation_config.p,
                            "top_k": self.generation_config.k,
                            "max_output_tokens": self.generation_config.max_output_tokens,
                            "response_mime_type": self.generation_config.response_mime_type
                            }
       

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name=self.model_name, generation_config=self.config_dict, system_instruction=self.system_instruction)

        except Exception as e:
            print(f"Failed to initialize Gemini Model: {e}")

    def generate_response(self, input_text, input_img):
        """ Generates a response out of a prompt and image (optional) using the Gemini flash model, and save to file"""
        try:
            img = Image.open(input_img)
            response = self.model.generate_content([input_text, img], stream=True)
            response.resolve()
            # Save the output to a file
            with open("data/output/phishing_email.html", "w", encoding="utf8") as file:
                file.write(response.text)

            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
        


