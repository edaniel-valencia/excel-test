# 👥 Sistema de Gestión y Carga de Clientes

<p align="center">
  <img src="img/logo-adavam.png" width="120" alt="Logo Adavam">
</p>

Bienvenido al repositorio del Sistema de Gestión de Clientes, desarrollado por **E. Daniel Valencia de Adavam**. Este proyecto es una solución moderna, rápida y escalable para la carga, lectura y gestión masiva de usuarios a través de archivos Excel y CSV, respaldado por una base de datos relacional.

---

## 🚀 Guía de Implementación para Desarrolladores

Este proyecto fue diseñado para ser fácil de comprender, levantar y escalar por desarrolladores de cualquier nivel. A continuación, encontrarás los pasos necesarios para desplegarlo en tu entorno local.

### 1. Requisitos Previos
- **Python 3.9 o superior**
- **PostgreSQL** instalado y ejecutándose en tu máquina.
- **Git** (Opcional, para clonar y llevar control de versiones).

### 2. Configuración de la Base de Datos
El proyecto utiliza PostgreSQL por su robustez e integridad referencial. Para inicializar la base de datos:
1. Crea una nueva base de datos en PostgreSQL (por ejemplo, `excel_test`).
2. Ejecuta el script SQL incluido en el proyecto (`database_postgres.sql`) en tu motor de base de datos para crear la tabla `clientes` y cargar datos iniciales de prueba.
3. Edita el archivo `.env` en la raíz del proyecto con tus credenciales de acceso:
   ```env
   DATABASE_URL=postgresql://tu_usuario:tu_contraseña@localhost:5432/excel_test
   ```

### 3. Configuración del Entorno Virtual
Es obligatorio y altamente recomendado utilizar un entorno virtual (venv) para no ensuciar las librerías globales de tu sistema operativo y evitar conflictos de versiones:

```bash
# Crear el entorno virtual en la carpeta del proyecto
python3 -m venv venv

# Activar el entorno virtual (Mac/Linux)
source venv/bin/activate

# Activar el entorno virtual (Windows PowerShell)
# .\venv\Scripts\Activate.ps1

# Instalar todas las dependencias necesarias
pip install -r requirements.txt
```

### 4. Ejecución del Proyecto (2 Terminales)

El sistema está desacoplado, por lo que se compone de dos piezas que deben correr simultáneamente: el Backend y el Frontend.

**Terminal 1: Backend (FastAPI)**
```bash
# Asegúrate de tener el venv activado
source venv/bin/activate
uvicorn main:app --reload
```
*El servidor backend (API REST) quedará escuchando en `http://localhost:8000`.*

**Terminal 2: Frontend (Streamlit)**
Abre una nueva pestaña en tu terminal:
```bash
# Activa el entorno virtual en esta nueva pestaña también
source venv/bin/activate
streamlit run app.py
```
*La interfaz gráfica se abrirá automáticamente en tu navegador web.*

### 5. Control de Versiones y Seguridad (.gitignore)
Para mantener las buenas prácticas de desarrollo y seguridad, este proyecto incluye un archivo `.gitignore`. 
**NUNCA se deben subir al repositorio (Git)** los siguientes archivos y carpetas:
- **`venv/`**: El entorno virtual es pesado y depende del sistema operativo de cada desarrollador.
- **`.env`**: Contiene tus contraseñas y credenciales reales de la base de datos. Cada desarrollador debe crear su propio `.env` local.
- **Archivos de caché**: Como `__pycache__` o `.DS_Store`.

---

## 🏗️ Arquitectura y Patrón MVC

El sistema está construido utilizando una arquitectura moderna de **servicios desacoplados** (Frontend y Backend separados). Aunque este es un modelo cliente-servidor distribuido, podemos trazar un claro paralelismo con el patrón de diseño **MVC (Modelo-Vista-Controlador)**:

- **Modelo (Model):** Representado por `SQLAlchemy` dentro de `main.py` y la base de datos PostgreSQL. Se encarga de definir la estructura exacta de la tabla `clientes`, las validaciones de tipos de datos, y ejecutar las consultas reales en lenguaje SQL por debajo de la mesa.
- **Controlador (Controller):** Representado por `FastAPI` (`main.py`). Actúa como el "cerebro" o intermediario. Expone las rutas de comunicación (Endpoints REST como `/upload` y `/clientes`), recibe los archivos enviados por la Vista, procesa la lógica de extracción de datos masivos usando la librería `pandas`, y le ordena al Modelo que guarde la información.
- **Vista (View):** Representado por `Streamlit` (`app.py`). Es la interfaz gráfica pura. Su única responsabilidad es dibujar en la pantalla (botones, tablas, menús), atrapar las interacciones del usuario y enviarlas al Controlador por medio de peticiones HTTP.

### 📂 Estructura del Proyecto
```text
excel-test/
├── app.py                  # [VISTA] Interfaz gráfica de usuario construida con Streamlit
├── main.py                 # [CONTROLADOR/MODELO] Servidor backend construido con FastAPI
├── database_postgres.sql   # Script de inicialización de la estructura y volcado de DB
├── requirements.txt        # Manifiesto de dependencias de Python
├── .env                    # Archivo de variables de entorno (Conexión a DB)
└── img/                    # Directorio de recursos gráficos
    └── logo-adavam.png     # Logo utilizado en la barra lateral e inicio
```

## 🔌 Conexión a la Base de Datos

El flujo de conexión a los datos se maneja a través de la librería **SQLAlchemy**, que funciona como un ORM (Mapeo Objeto-Relacional):

1. **Seguridad:** El archivo `.env` almacena la cadena de conexión de manera segura (este archivo nunca debe subirse a repositorios públicos como GitHub).
2. **Carga en Memoria:** `main.py` lee esta variable utilizando la librería `python-dotenv`.
3. **Gestión de Sesiones:** SQLAlchemy crea un motor de base de datos (`engine`) y una fábrica de sesiones (`SessionLocal`). Cada vez que un usuario pide ver la lista o cargar un archivo, se abre una sesión temporal, se ejecuta la acción, y **se cierra de inmediato**, garantizando que las conexiones sean limpias y evitando fugas de memoria en PostgreSQL.

---
*Desarrollado y diseñado por **E. Daniel Valencia de Adavam** para potenciar a la comunidad de desarrolladores.*
