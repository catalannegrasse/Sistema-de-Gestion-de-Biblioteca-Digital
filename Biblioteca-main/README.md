# Biblioteca - UI

Pequeña interfaz web en Flask para interactuar con `biblioteca.py`.

Requisitos:

- Python 3.8+
- Instalar dependencias: `pip install -r requirements.txt`

Instrucciones para ejecutar (local):

```bash
python -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Abrir http://127.0.0.1:5000

Subir a GitHub (pasos desde la carpeta del proyecto):

```bash
git init
git add .
git commit -m "Agregar frontend Flask para biblioteca"
# Crear repo en GitHub (manual o con GitHub CLI)
# Por ejemplo con gh (si está instalado):
# gh repo create NOMBRE_REPO --public --source=. --remote=origin
# Luego:
# git push -u origin main
```
