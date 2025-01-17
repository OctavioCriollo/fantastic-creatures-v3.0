import os
import random
import segno
from PIL import Image
import io
from sqlalchemy.orm import Session
from app.models.models import Wheel
from app.database import get_db
from datetime import datetime

STATIC_CREATURES_QR_CODE_PATH = os.path.join(os.getcwd(), 'static', 'qr_codes')
os.makedirs(STATIC_CREATURES_QR_CODE_PATH, exist_ok=True)

def calculate_life_number(birth_date):
    digits = [int(digit) for digit in birth_date.replace('-', '') if digit.isdigit()]
    life_number = sum(digits)
    while life_number > 9:
        life_number = sum(int(digit) for digit in str(life_number))
    return life_number

def calculate_name_number(name):  
    name_number = 0
    for char in name:
        # Get the ASCII code of the character
        ascii_code = ord(char)
        # Use modulo 9 and add 1 to get a number between 1 and 9
        char_value = (ascii_code % 9) + 1
        name_number += char_value
    while name_number > 9:
        name_number = sum(int(digit) for digit in str(name_number))
    return name_number

async def generate_qr_code(creature, client_name, birth_date):
    qr_data = f"No escanees mis secretos"
    qr = segno.make(qr_data, error='h')

    img_size = (300, 300)
    img = Image.new('RGB', img_size, color='white')

    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=5)
    buffer.seek(0)
    qr_img = Image.open(buffer)

    qr_size = 250
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    qr_position = ((img_size[0] - qr_size) // 2, (img_size[1] - qr_size) // 2)
    img.paste(qr_img, qr_position)

    image_filename = f"QR_Code_{creature.name}.png".replace(" ", "_")
    qr_file_path = os.path.join(STATIC_CREATURES_QR_CODE_PATH, image_filename)

    img.save(qr_file_path)

    return image_filename

async def spin_wheel():
    db = next(get_db())
    count = db.query(Wheel).count()
    
    if count == 0:
        raise ValueError("Sorry there are no creatures available NOW")

    random_index = random.randint(0, count - 1)
    wheel_entry = db.query(Wheel).offset(random_index).first()
    wheel_number = wheel_entry.numero

    return wheel_number

