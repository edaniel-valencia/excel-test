import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestión de Clientes", page_icon="👥", layout="wide")

import time

# ==========================================
# PANTALLA DE CARGA (LOADING)
# ==========================================
if "loaded" not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    # Contenedor centrado para el loading
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("") # Espacio superior
        st.write("")
        st.write("")
        st.image("img/logo-adavam.png", use_container_width=True)
        
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        # Simular carga del 1 al 100%
        for percent_complete in range(101):
            time.sleep(0.015) # Ajusta la velocidad aquí
            progress_bar.progress(percent_complete)
            progress_text.markdown(f"<div style='text-align: center; color: gray;'>Cargando sistema... {percent_complete}%</div>", unsafe_allow_html=True)
            
        time.sleep(0.5)
        st.session_state.loaded = True
        st.rerun()

# URL de nuestra API en FastAPI
API_URL = "http://localhost:8000"

# ==========================================
# MENÚ LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    # Mostrar logo en la barra lateral
    st.image("img/logo-adavam.png", use_container_width=True)
    
    st.markdown("---")
    
    # Opciones de navegación
    menu_seleccionado = st.radio(
        "Navegación",
        ["Cargar Usuarios", "Leer Usuarios"]
    )
    
    st.markdown("---")
    
    # Footer
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 20px;'>"
        "Desarrollado por <b>E. Daniel Valencia</b> de Adavam"
        "</div>", 
        unsafe_allow_html=True
    )

# ==========================================
# RENDERIZADO PRINCIPAL (Evita errores de React)
# ==========================================
main_content = st.empty()

with main_content.container():
    if menu_seleccionado == "Cargar Usuarios":
        st.title("⬆️ Cargar Usuarios")
        st.markdown("Sube tu archivo **CSV o Excel** para importar clientes a la base de datos PostgreSQL de forma sencilla.")

        uploaded_file = st.file_uploader("Selecciona un archivo CSV o Excel", type=["csv", "xlsx", "xls"], key="uploader")

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df_preview = pd.read_csv(uploaded_file, sep=';')
                else:
                    df_preview = pd.read_excel(uploaded_file)
                
                st.write("Vista previa de los datos:")
                st.dataframe(df_preview.head())
                
                if st.button("Cargar a la Base de Datos", type="primary", key="btn_cargar"):
                    with st.spinner("Subiendo datos..."):
                        uploaded_file.seek(0)
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "multipart/form-data")}
                        try:
                            response = requests.post(f"{API_URL}/upload", files=files)
                            if response.status_code == 200:
                                st.success(response.json().get("mensaje", "Datos cargados exitosamente."))
                            else:
                                st.error(f"Error al cargar los datos: {response.text}")
                        except requests.exceptions.ConnectionError:
                            st.error("❌ No se pudo conectar al servidor FastAPI. Por favor, asegúrate de haber arrancado el backend en la terminal.")
            except Exception as e:
                st.error(f"No se pudo leer el archivo: {e}")

    elif menu_seleccionado == "Leer Usuarios":
        st.title("📋 Lista de Usuarios Registrados")
        st.markdown("A continuación se muestran los clientes guardados en la base de datos.")

        # Botón de refrescar (al hacer clic, Streamlit recarga la página por defecto)
        st.button("🔄 Refrescar Lista", type="primary", key="btn_refrescar")

        # Carga automática de los datos
        with st.spinner("Cargando clientes desde la base de datos..."):
            try:
                response = requests.get(f"{API_URL}/clientes")
                if response.status_code == 200:
                    clientes = response.json()
                    if isinstance(clientes, dict) and "error" in clientes:
                        st.error(f"Error en la base de datos: {clientes['error']}")
                    elif len(clientes) > 0:
                        df_clientes = pd.DataFrame(clientes)
                        st.dataframe(df_clientes, use_container_width=True)
                    else:
                        st.info("No hay clientes registrados en la base de datos.")
                else:
                    st.error("No se pudo conectar con la API.")
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar al servidor FastAPI. Por favor, asegúrate de haber arrancado el backend en la terminal.")
