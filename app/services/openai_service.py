import os
import requests
from openai import OpenAI
from app.config import settings
from app.services.utils_service import calculate_life_number, calculate_name_number, spin_wheel
from app.services.dalle_service import AI_image_creature_generator # Update: Changed import statement
from datetime import datetime

STATIC_CREATURES_IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'creatures')
os.makedirs(STATIC_CREATURES_IMG_PATH, exist_ok=True)

client_openAI = OpenAI(
    organization=settings.OPENAI_ORG_ID,
    project=settings.OPENAI_PROJECT_ID,
)

async def AI_description_creature_generator(client_name, birth_date, creature_details):
    birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')
    life_number = calculate_life_number(birth_date)
    name_number = calculate_name_number(client_name)

    rarity = "Legendaria" if life_number > 5 else "Común"
    power = "Alta" if name_number in [1, 3, 7] else "Media"


    prompt = f"""
        Eres un creador de criaturas mágicas únicas, mitológicas, prehistóricas. Crea una criatura imaginativa basada en los siguientes detalles:

        - Relación con el usuario: El usuario {client_name} quiere una criatura que tenga una conexión especial con ellos.
        - Fecha de nacimiento del usuario: {birth_date} (Número de Vida: {life_number})
        - Detalles adicionales sobre la criatura: {creature_details}
        
        Si el usuario especifica múltiples criaturas o características en {creature_details}, combina sus rasgos para crear una nueva criatura híbrida. 
        Imagina que estás creando esta criatura genéticamente, mezclando las características de todas las criaturas mencionadas para crear 
        una entidad única que represente los deseos del usuario y que tenga una apariencia perfecta y no horrible.

        El nombre de la criatura, inventarlo, no uses el {client_name} para inventar el nombre.
        Proporciona una descripción detallada de la criatura resultante, incluyendo:
        - Apariencia física.
        - Habilidades especiales o mágicas.
        - Personalidad o comportamiento.
        - detalles astrológicos de la criatura en base a {birth_date} (eso no significa que nació en esa fecha pues las criaturas son muy antiguas).

        Proporciona la respuesta en formato:
        Nombre: [nombre de la criatura]
        Descripción: [descripción de la criatura] (no debe tener mas de 300 palabras).

        Que [descripción de la criatura] parezca que estas contando una historia a {client_name} quien puede tener entre 2 a 8 años de edad.
    """

    prompt2 = f"""
        Eres un creador de criaturas mágicas y míticas únicas. Crea una criatura imaginativa basada en los siguientes detalles:

        - Relación con el usuario: El usuario {client_name} quiere una criatura especial que sea su compañera mágica, alguien con quien pueda compartir secretos y aventuras.
        - Fecha de nacimiento del usuario: {birth_date} (Número de Vida: {life_number})
        - Detalles adicionales sobre la criatura: {creature_details}

        Si el usuario menciona múltiples criaturas o características en {creature_details}, fusiona sus rasgos para crear una criatura híbrida única. 
        Imagina que estás creando esta criatura especialmente para el usuario, dándole una apariencia encantadora y amistosa.

        El nombre de la criatura debe ser inventado por ti, pero que suene mágico y único, sin usar el nombre del usuario.

        Proporciona una descripción detallada de la criatura, incluyendo:
        - Cómo se ve (colores, forma, detalles únicos).
        - Habilidades mágicas o especiales que tiene.
        - Personalidad o cómo interactúa con el usuario {client_name}.
        - Conexión astrológica (basada en la fecha de nacimiento del usuario, pero recuerda que las criaturas pueden ser muy antiguas).

        Por favor, entrega la respuesta en este formato:
        Nombre: [nombre mágico de la criatura]
        Descripción: [Cuenta una historia detallada pero que no exceda de 300 palabras, como si estuvieras contándosela a {client_name}, quien puede tener entre 2 y 8 años 
        de edad. La historia debe ser mágica, suave, y emocionante, asegurándote de que la criatura sea amistosa y especial para el usuario].
    """

    prompt3 = f"""
        Eres un creador de criaturas mágicas, míticas y únicas. Tu misión es crear una criatura que sea mucho más que una compañera: una amiga mágica, alguien que siempre estará a tu lado, acompañándote en tus aventuras y compartiendo contigo secretos y sueños emocionantes. Esta criatura es especial para {client_name}.

        - Relación con el usuario: {client_name} desea una criatura mágica que le acompañe en todas sus aventuras, esté a su lado en los momentos de alegría y calma, y sea un amigo fiel en quien siempre pueda confiar.
        - Fecha de nacimiento del usuario: {birth_date} (Número de Vida: {life_number}).
        - Detalles adicionales sobre la criatura: {creature_details}.

        Si el usuario menciona varias criaturas o características en {creature_details}, toma esos rasgos y combínalos para crear una criatura híbrida increíble, con una apariencia mágica que fascine y emocione a {client_name}. Esta criatura debe ser hermosa y amigable, alguien con quien pueda soñar, jugar y sentir una conexión especial.

        El nombre de la criatura lo debes inventar tú, y debe sonar único, mágico y especial. No utilices el nombre del usuario para nombrar la criatura.

        Crea una descripción que capture la magia de esta criatura, contando su historia como si estuvieras hablándole directamente a {client_name}, que tiene entre 2 y 8 años. La criatura debe ser su compañera perfecta, con habilidades asombrosas, una personalidad encantadora, y un aspecto tan maravilloso que {client_name} quiera tenerla siempre a su lado.

        - Describe su apariencia de manera mágica y detallada: ¿Cómo se ve? (colores, forma, detalles únicos que la hagan especial).
        - Explica las habilidades mágicas o especiales que tiene: ¿Qué puede hacer que la hace tan increíble para {client_name}?
        - Describe su personalidad: ¿Es juguetona, protectora, curiosa? ¿Cómo interactúa con {client_name} en sus aventuras?
        - Incluye una conexión astrológica basada en la fecha de nacimiento del usuario, pero recuerda que las criaturas son antiguas y su sabiduría y magia han perdurado a lo largo del tiempo.

        Por favor, entrega la respuesta en el siguiente formato:

        Nombre: [nombre mágico de la criatura]
        Descripción: [Cuenta una historia mágica y emocionante de no más de 300 palabras, como si le estuvieras hablando a {client_name} directamente bajo el cielo estrellado. La narrativa debe ser suave y envolvente, asegurando que esta criatura se convierta en el amigo mágico y especial que {client_name} siempre ha soñado].
    """

    chat_completion = client_openAI.chat.completions.create(
        model="gpt-4",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "Eres un experto creador experto de criaturas mágicas, mitologicas y fantásticas."},
            {"role": "user", "content": prompt3}  # Usando prompt3 como en el original, pero puedes cambiarlo si es necesario
        ]
    )

    generated_text = chat_completion.choices[0].message.content.strip()
    print(f"Respuesta completa del modelo: {generated_text}")
    
    try:
        name_start = generated_text.index("Nombre: ") + len("Nombre: ")
        description_start = generated_text.index("Descripción: ")

        creature_name = generated_text[name_start:description_start].strip()
        creature_description = generated_text[description_start + len("Descripción: "):].strip()
    except ValueError:
        creature_name = "Unknown Creature"
        creature_description = generated_text

    unique_number = await spin_wheel()
    
    try:
        image_url = await AI_image_creature_generator(creature_description)
        if not image_url:
            raise ValueError('Error al generar la imagen: URL de imagen vacía o inválida.')
        
        # Download and save the image
        image_data = requests.get(image_url).content
        image_filename = f"{creature_name}_{unique_number}.png".replace(" ", "_")
        image_filepath = os.path.join(STATIC_CREATURES_IMG_PATH, image_filename)

        print("Nombre image creature guiones bajos:", image_filename)

        with open(image_filepath, 'wb') as image_file:
            image_file.write(image_data)

    except Exception as e:
        print(f"Error al generar la imagen de la criatura: {str(e)}")
        raise ValueError('Ocurrió un error al generar la imagen de la criatura.')

    return {
        'name': creature_name,
        'description': creature_description,
        'unique_number': unique_number,
        'image_url': image_filename
    }

