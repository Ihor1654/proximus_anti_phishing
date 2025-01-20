import os
import google.generativeai as genai
# pip install -q -U google-generativeai

from PIL import Image
# pip install -q -U pillow

class GeminiPhish:
    def __init__(self, model_name,generation_config, system_instruction):
        self.model_name = model_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.generation_config = generation_config
        self.system_instruction = system_instruction

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name=self.model_name, generation_config=self.generation_config, system_instruction=self.system_instruction)

        except Exception as e:
            print(f"Failed to initialize Gemini Model: {e}")

    def generate_response(self, input_text, input_img):
        """ Generates a response out of a prompt and image (optional) using the Gemini flash model, and save to file"""
        try:
            img = Image.open(input_img)
            response = self.model.generate_content([input_text, img], stream=True)
            response.resolve()
            # Save the output to a file
            with open("phishing_email.html", "w", encoding="utf8") as file:
                file.write(response.text)

            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None