from enum import Enum
import qrcode
from PIL import Image
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json

class Role(Enum):
    user:str = "user"
    admin:str = "admin"
    organization:str = "organization"

def get_user_role(role:Role) -> str:
    match role:
        case Role.admin:
            return "admin"
        case Role.user:
            return "user"
        case Role.organization:
            return "Organization"
        case _:
            return None
        
      



@dataclass
class QRcodeGenerator:
    data:str
    image_pa:Optional[str]=None
    def generate_qrcode(self):
        qr_image = qrcode.make(self.data)
        return qr_image.save('qrcode.png')

@dataclass
class PasswordHashAndCheck:
    user_password:str
    hashed_password:Optional[str]= None

    def password_hash(self) -> tuple[str]:
        return (self.user_password, self.hashed_password)

        


       



        