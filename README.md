 ```bash
/FastAPICreatureApp
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── creatures.py
│   │       └── payments.py
│   └── services/
│       ├── __init__.py
│       ├── utils_service.py
│       ├── openai_service.py
│       ├── image_service.py
│       ├── qr_service.py
│       ├── wheel_service.py
│       └── stripe_service.py
│
├── migrations/
│   └── ...
│
├── static/
│   ├── creatures/
│   │   └── ...
│   └── qr_codes/
│       └── ...
│
├── tests/
│   └── ...
│
├── .env
├── .gitignore
├── alembic.ini
├── database-alembic.py
├── Dockerfile
├── Dockerfile.alembic
├── main.py
├── requirements.txt
└── README.md
```

# Crear un entorno virtual
```bash
python -m venv .venv
```
# Activar el entorno virtual
```bash
source .venv/bin/activate
```
# Instalar fastapi 
```bash
pip install fastapi
```
# Instalar uvicorn
```bash
pip install uvicorn
```
# Instalar las dependencias Iniciales
```bash
pip install sqlalchemy
pip install pydantic
pip install python-dotenv
```
# Instalar las dependencias de requirements.txt
```bash
pip install -r requirements.txt
``` 

# Crear requeriments.txt
```bash
pip freeze > requirements.txt
```  
# Verificar paquetes actualizados
```bash
pip list --outdated
```  
# Actualizar paquetes del archivo requeriments.txt
```bash
pip install --upgrade pip pip-tools
mv requirements.txt requirements.in
pip-compile --upgrade requirements.in
pip install -r requirements.txt
```  
# Sincronizar paquetes del archivo requeriments.txt
```bash
pip-sync requirements.txt
```  

# Crear el directorio principal
```bash
mkdir root-directory
cd root-directory
```
# Crear la estructura de directorios
```bash
mkdir -p app/models app/schemas app/api/endpoints app/services static/qr_codes migrations
```

# Crear archivos principales
```bash
touch app/__init__.py app/main.py app/config.py app/database.py
touch app/models/__init__.py app/models/models.py
touch app/schemas/__init__.py app/schemas/schemas.py
touch app/api/__init__.py app/api/dependencies.py
touch app/api/endpoints/__init__.py app/api/endpoints/creature.py app/api/endpoints/client.py
touch app/services/__init__.py app/services/openai_service.py app/services/qr_service.py
touch alembic.ini .env requirements.txt
```

# Crear un archivo README.md (opcional, pero recomendado)
```bash
touch README.md
```