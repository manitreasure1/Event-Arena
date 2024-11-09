from enum import Enum
import qrcode
from PIL import Image
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json

class Role(Enum):
    user:str
    admin:str
    organization:str


@dataclass
class QRcodeGenerator:
    data:str
    image_pa:Optional[str]=None
    def generate_qrcode(self):
        qr_image = qrcode.make(self.data)
        return qr_image.save('qrcode.png')

