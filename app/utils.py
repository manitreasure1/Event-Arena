from enum import Enum
import qrcode
from PIL import Image
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.extentions import db
from app.database import Role
import smtplib
from dotenv import load_dotenv
import ssl
import os
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()


class SetRole(Enum):
    user:str = "user"
    admin:str = "admin"
    organization:str = "organization"


def get_user_role(role:SetRole) -> str:
    match role:
        case SetRole.admin:
            return "admin"
        case SetRole.user:
            return "user"
        case SetRole.organization:
            return "Organization"
        case _:
            return None
        

def create_initial_roles():
    initial_roles = {
        1: {'name': 'admin', 'description': 'Administrator with full access'},
        2: {'name': 'user', 'description': 'Regular user with limited access'},
        3: {'name': 'organization', 'description': 'Organization-level access'},
    }
    for role_id, role_data in initial_roles.items():
        role = Role(role_id=role_id, name=role_data['name'], description=role_data['description'])
        db.session.add(role)
    db.session.commit() 

def check_empty_role():
    role = db.session.query(Role).all()
    if not role:
        create_initial_roles()
    
    

@dataclass
class QRcodeGenerator:
    data:str
    image_pa:Optional[str]=None
    def generate_qrcode(self):
        qr_image = qrcode.make(self.data)
        return qr_image.save('qrcode.png')


def username(username:str) -> str:
    return username.split('@')[0]



def send_email(username:str, verification_token:str, reciever_email:str):
    sender_email = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')

    with open("email_file.md", 'r') as email_file:
        template = Template(email_file.read())
        msg = template.render(username, verification_token)
        msg = MIMEMultipart()

        msg['Subject'] = "Validate your email"
        msg['From'] = send_email
        msg['To'] = reciever_email

        msg.attach(MIMEText(msg, 'plain'))
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.starttls()
                server.login(sender_email, email_password)
                server.send_message(msg)
        except Exception as e:
            print(e)
            raise




