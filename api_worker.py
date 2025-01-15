from gophish import Gophish
from gophish.models import *
from dotenv import load_dotenv
import os 
import csv
import urllib3



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Api_Worker:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api = Gophish(self.api_key,host="https://127.0.0.1:3333",verify = False)
        self.targets = []
        self.groups = []
        self.page = None
        self.smtp = SMTP(name='Test')
        self.url = 'www.google.com' 
        self.template = None   
        self.Campaign_counter = 0  
        self.template_counter = 0
        self.id = int(input('id')) 
        self.app_pass = os.getenv('APP_PASS')
        self.mail = os.getenv('EMAIL')
        
    
    def load_targets_from_csv(self, file_path="test_targets.csv"):
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file) 
                for row in csv_reader:
                    first_name = row.get('first_name')
                    last_name = row.get('last_name')
                    email = row.get('email')

                    if first_name and last_name and email:  
                        user = User(first_name=first_name, last_name=last_name, email=email)
                        self.targets.append(user)  
                    else:
                        print(f"String  {row} is missing ")
            print(f"{len(self.targets)} Successfully loaded from {file_path}")
        except FileNotFoundError:
            print(f"File {file_path} is not founded.")
        except Exception as e:
            print(f"Error while reading the file: {e}")


    def manualy_create_group(self):
        name = input('Group name:')
        group = Group(name=name,targets = self.targets)
        print(self.api_key)
        group = self.api.groups.post(group)
        self.groups.append(group)
        
    def create_tamplate(self):
        self.template = Template(name=f"Example Template#{self.template_counter+self.id}",
                    subject="Phishing Test",
                    html="<html><body><h1>This is a test</h1></body></html>")   
        self.template = self.api.templates.post(self.template)

    def create_page(self):
        #Inside we gona get the generative html tamplate
        self.page = Page(
        name=f"Example Landing Page {self.id}",
        html="<html><body><h1>This is a phishing page</h1></body></html>"
        )
        self.page = self.api.pages.post(self.page)
        
    def create_Champaign(self):
        campaign = Campaign(
            name=f'Example Campaign#{self.Campaign_counter+self.id}', groups=self.groups, page=self.page,
                template=self.template, smtp=self.smtp)
        self.campaign = self.api.campaigns.post(campaign)

    def create_smtp(self):
        self.smtp = SMTP(
            name=f"Example SMTP {self.id}",
            host="smtp.gmail.com",
            interface_type="SMTP",
            from_address = self.mail,
            username = self.mail,      
            password = self.app_pass
            
        )
        self.smtp = self.api.smtp.post(self.smtp)


        


