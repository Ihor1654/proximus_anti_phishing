from gophish import Gophish
from gophish.models import *
from dotenv import load_dotenv
import os 
import csv
import urllib3
import db_worker as db


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Api_Worker:
    def __init__(self,campaign_name:str):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api = Gophish(self.api_key,host="https://127.0.0.1:3333",verify = False)
        self.targets = []
        self.groups = []
        self.group_id = None
        self.page = None
        self.smtp = None
        self.url = 'www.google.com' 
        self.template = None   
        self.campaign = None
        self.campaign_name = campaign_name
        self.Campaign_counter = 0  
        self.template_counter = 0
        # self.id = int(input('id')) 
        self.app_pass = os.getenv('APP_PASS')
        self.mail = os.getenv('EMAIL')
        self.db_worker = db.DBWorker()
        self.create_campaign_db()
        self.create_smtp()
        self.create_page()

    

    def create_group_db(self):
        group = self.db_worker.add_record(db.Group,name = f'Group for {self.campaign_name}')
        self.group_id = group.group_id
        return group.group_id
    
    def create_config(self):
        config = self.db_worker.add_record(db.GenerativeConfig, 
                                             temperature=25, 
                                             p=1.25, 
                                             k=10, 
                                             max_output_tokens=1000, 
                                             response_mime_type="application/json")
        return config.id
    
    
    def create_theme(self):
        theme = self.db_worker.add_record(db.Theme, 
                                 name="Theme_name", 
                                 landing_page="<html><body><h1>This is a phishing page</h1></body></html>", 
                                 system_instruction="System instructions here", 
                                 structur_instruction="Structure instructions here", 
                                 prompt_template="Prompt template text", 
                                 subject="New subject", 
                                 config_id=self.create_config())
        return theme.id
    
    def reset_properties(self):
        self.campaign = None
        self.groups = []
        self.template = None
        self.targets = []
        print(self.campaign )
        print(self.groups)
        print(self.template)

    def create_campaign_db(self):
        campaign = self.db_worker.add_record(db.Campaign,name = self.campaign_name,group_id = self.create_group_db(),theme_id = self.create_theme())
        self.campaign = campaign
    
    def create_page(self):
        #Inside we gona get the generative html tamplate
        self.page = Page(
        name=f"Example Landing Page for {self.campaign_name}",
        html= self.db_worker.get_record(db.Theme,id=self.campaign.theme_id).landing_page
        )
        self.page = self.api.pages.post(self.page)

    def create_smtp(self):
        self.smtp = SMTP(
            name=f"Example SMTP {self.campaign_name}",
            host="smtp.gmail.com",
            interface_type="SMTP",
            from_address = self.mail,
            username = self.mail,      
            password = self.app_pass,
            port=587,
            tls=True 
            
        )
        self.smtp = self.api.smtp.post(self.smtp)

    
    
    def load_targets_from_csv(self, file_path="test_targets.csv"):
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file) 
                for row in csv_reader:
                    first_name = row.get('first_name')
                    last_name = row.get('last_name')
                    email = row.get('email')
                    company = row.get('company')
                    business_unit = row.get('business_unit')
                    team = row.get('team')
                    role = row.get('role')
                    linkedin = row.get('linkedin')
                    if first_name and last_name and email:
                        user_db = self.db_worker.add_record(db.User, firstname=first_name, lastname=last_name, company=company,
                                business_unit=business_unit, team=team, role=role,
                                email=email, linkedin=linkedin)
                        user_gp = User(first_name=first_name, last_name=last_name, email=email)
                        self.targets.append(user_gp)

                        self.db_worker.add_user_to_group(user_id=user_db.id,group_id=self.group_id)
                        self.create_group(user_db.id)
                        self.create_tamplate(user_db.id)
                        self.create_Champaign(user_db.id)
                        self.reset_properties()
                        
                    else:
                        print(f"String  {row} is missing ")
            print(f"{len(self.targets)} Successfully loaded from {file_path}")
        except FileNotFoundError:
            print(f"File {file_path} is not founded.")
        except Exception as e:
            print(f"Error while reading the file: {e}")


    def create_group(self,user_id):
        name = f'Group {self.campaign_name}_{user_id}'
        group = Group(name=name,targets = self.targets)
        print(self.api_key)
        group = self.api.groups.post(group)
        self.groups.append(group)
        
    def create_tamplate(self,user_id):
        self.template = Template(name=f"Example Template for User {user_id}",
                    subject="Phishing Test",
                    html="<html><body><h1>This is a test</h1></body></html>")   
        self.template = self.api.templates.post(self.template)

    
        
    def create_Champaign(self,user_id):
        campaign = Campaign(
            name=f'Example Campaign#{self.campaign_name}_{user_id}', groups=self.groups, page=self.page,
                template=self.template, smtp=self.smtp)
        self.campaign = self.api.campaigns.post(campaign) 
        



        


