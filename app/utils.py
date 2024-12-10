from enum import Enum
import qrcode
from PIL import Image
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.extentions import db
from app.database import Role


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





