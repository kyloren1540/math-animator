# Math Animator

Visualizador educativo de funciones matemáticas con gráficas interactivas, ejemplos predefinidos y análisis (dominio, rango, raíces, intersecciones).

## Versión web (enlace público)

La app web usa **Streamlit** y se puede publicar gratis en [Streamlit Community Cloud](https://streamlit.io/cloud).

### Publicar en 5 pasos

1. **Crea un repositorio en GitHub** (vacío, por ejemplo `math-animator`).

2. **Sube este proyecto** desde la carpeta del proyecto:

   ```bash
   git init
   git add .
   git commit -m "Math Animator: app web y escritorio"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/math-animator.git
   git push -u origin main
   ```

3. Entra en [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.

4. Pulsa **New app** y configura:
   - **Repository:** tu repo
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`

5. Pulsa **Deploy**. En unos minutos tendrás un enlace como:

   `https://math-animator-xxxxx.streamlit.app`

Comparte ese enlace: cualquiera podrá usar la app en el navegador sin instalar nada.

### Probar en local (web)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Se abrirá en `http://localhost:8501`.

## Versión de escritorio (PyQt)

```bash
pip install -r requirements-desktop.txt
python main.py
```

## Estructura

| Archivo | Uso |
|---------|-----|
| `streamlit_app.py` | App web para Streamlit Cloud |
| `main.py` | App de escritorio |
| `functions/` | Tipos de funciones y ejemplos |
| `graph/` | Motor de gráficas matplotlib |

## Licencia

Uso educativo libre.
