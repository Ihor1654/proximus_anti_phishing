from gophish import Gophish

from gophish.models import *
from time import sleep
from dotenv import load_dotenv
import os 
import csv
import urllib3

from template_creator import TemplateCreator

import db_worker as db
load_dotenv()




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Api_Worker:

    def __init__(self,):
        self.api_key = os.getenv('API_KEY')
        self.api = Gophish(self.api_key,host="https://127.0.0.1:3333",verify = False)
        self.app_pass = os.getenv('APP_PASS')
        self.mail = os.getenv('EMAIL')
        self.url = 'www.google.com' 
        self.template = None   
        self.db_worker = db.DBWorker()
        
=======
    def post_tamplate_for_user(self,user_id,theme_id:int=1):
        try:
            template = self.db_worker.get_record(db.Template,user_id=user_id)
            theme = self.db_worker.get_record(db.Theme,id=theme_id)
            self.template = Template(name=f"Example Template for User {user_id}",
                        subject=theme.subject,
                        html=template.html_template)   
            self.template = self.api.templates.post(self.template)
        except Exception as e:
            print('Template is not founded')


    def get_tamplate_by_id(self,template_id):
        template = self.api.templates.get(template_id=template_id)
        return template

    def delete_template_by_id(self,template_ids:list):
        for template_id in template_ids:
            self.api.templates.delete(template_id)


    def post_smtp_for_campaign(self,campaing_id):
        smtp = SMTP(
            name=f"SMTP  for Campaign#{campaing_id}",
            host="smtp.gmail.com",
            interface_type="SMTP",
            from_address = self.mail,
            username = self.mail,      
            password = self.app_pass,
            port=587,
            tls=True   
        )
        self.api.smtp.post(smtp)

    def post_group(self,campaing_id,user_ids:list):
        target_list = []
        campaign_name = self.db_worker.get_record(db.Campaign,id=campaing_id).name
        match len(user_ids):
            case 1:
                name = f"Group for {campaign_name}_{user_ids[0]}" 
            case _:
                name = f'Group for {campaign_name}'
        for user_id in user_ids:
            user = self.db_worker.get_record(db.User,id=user_id)
            user_gp = User(first_name=user.firstname,last_name=user.lastname,email=user.email,position=user.role)
            target_list.append(user_gp)
        group = Group(name=name,targets=target_list)
        self.api.groups.post(group)

    def post_page(self,campaign_id):
        theme_id = self.db_worker.get_record(db.Campaign, id = campaign_id).theme_id
        page = Page(
        name=f"Landing Page for Campaign #{campaign_id}",
        html= self.db_worker.get_record(db.Theme,id=theme_id).landing_page
        )
        self.api.pages.post(page)

    def post_campaign(self,campaign_id,group_id:int ,template_id:int,smtp_id:int = 27,l_page_id:int = 31):
        groups = self.api.groups.get(group_id=group_id)
        
        template = self.api.templates.get(template_id=template_id)
        campaign_name = self.db_worker.get_record(db.Campaign,id=campaign_id).name
        campaign = Campaign(
            name=f'Example Campaign#{campaign_name}', groups=[groups], page=self.api.pages.get(page_id=l_page_id),
                template = template, smtp=self.api.smtp.get(smtp_id=smtp_id))
        self.api.campaigns.post(campaign) 

    def create_Champaign_for_user(self,user_id):
        campaign = Campaign(
            name=f'Example Campaign#{self.campaign_name}_{user_id}', groups=self.groups, page=self.page,
                template=self.template, smtp=self.smtp)
        self.api.campaigns.post(campaign)  