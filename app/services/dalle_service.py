import os
import requests
from app.config import settings
from openai import OpenAI

STATIC_CREATURES_IMG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'creatures')
os.makedirs(STATIC_CREATURES_IMG_PATH, exist_ok=True)

client_openAI = OpenAI(
    organization=settings.OPENAI_ORG_ID,
    project=settings.OPENAI_PROJECT_ID,
)

async def AI_image_creature_generator(description):
    prompt = f"""
        Crea una imagen altamente detallada y fotorrealista de una criatura única basada únicamente en su ***apariencia física*** descrita en {description}. 
        Ignora cualquier información sobre habilidades, poderes, vida o aspectos astrológicos. Concéntrate solo en las características físicas de la criatura, 
        como su tamaño, forma, textura de la piel, escamas, pelaje, plumas, colores, y otras características fisicas visibles.
        
        No incluyas ningún texto, título, símbolo, gráfico adicional, ni detalles que no formen parte del aspecto físico de la criatura.

        La criatura debe estar representada en una vista de cuerpo completo, mostrando todo su cuerpo de cabeza a cola, con todos sus rasgos distintivos y 
        texturas claramente visibles. No incluyas ningún texto, símbolos, gráficos adicionales, ni detalles que no formen parte del aspecto físico de la criatura.

        La criatura debe estar ambientada en un hábitat natural adecuado a sus características físicas, como un bosque denso, la cima de una montaña, 
        un desierto abrasador, o un océano profundo, según corresponda. El fondo debe estar ligeramente desenfocado para proporcionar profundidad sin distraer 
        la atención de la criatura. Asegúrate de que el entorno natural complemente y realce la apariencia de la criatura.

        La imagen final debe transmitir una sensación de asombro e intriga, capturando la esencia física de la criatura en un entorno realista y vívido, 
        sin distracciones de texto, gráficos o elementos artificiales.
        **NO DEBE HABER NINGÚN TEXTO EN LA IMAGEN FINAL**.
        """
    
    prompt_no_text = """
        NO TEXT. This image must contain NO TEXT, titles, symbols, or graphics of any kind.
        The creature is the ONLY focus of the image. There should be NO written language or characters anywhere in the image.
        """
                
    image_size = os.getenv('IMAGE_SIZE', '512x512')  # Usa el valor de .env o un valor predeterminado
    image_response = client_openAI.images.generate(
        model="dall-e-3",
        prompt=prompt + prompt_no_text,
        quality="standard",
        n=1,
        size=image_size   
        #size='1024x1024'    
    )
    image_url = image_response.data[0].url
       
    return image_url

