import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Telco Churn Analytics", layout="wide")

# --- CLASE DE PROCESAMIENTO (POO) ---
class DataAnalyzer:
    """Clase encargada de encapsular la lógica de análisis del dataset[cite: 107, 108]."""
    
    def __init__(self, data):
        self.df = data

    def get_info(self):
        """Retorna información general y nulos[cite: 46, 48]."""
        return self.df.dtypes, self.df.isnull().sum()

    def classify_variables(self):
        """Clasifica variables en numéricas y categóricas usando lógica de tipos[cite: 49, 54]."""
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        return numeric_cols, categorical_cols

    def plot_distribution(self, column):
        """Genera histogramas para variables numéricas[cite: 68, 69]."""
        fig, ax = plt.subplots()
        sns.histplot(self.df[column], kde=True, ax=ax, color='skyblue')
        ax.set_title(f"Distribución de {column}")
        return fig

    def plot_bivariate(self, cat_col, target='Churn'):
        """Análisis de variables categóricas vs Churn[cite: 80, 83]."""
        fig, ax = plt.subplots()
        sns.countplot(data=self.df, x=cat_col, hue=target, ax=ax, palette='viridis')
        ax.set_title(f"{cat_col} vs {target}")
        return fig

# --- INTERFAZ (SIDEBAR) ---
st.sidebar.title("Navegación")
modulo = st.sidebar.radio("Ir a:", ["Home", "Carga de Datos", "EDA"]) # [cite: 20]

# --- MÓDULO 1: HOME ---
if modulo == "Home":
    st.title("Proyecto: Análisis de Fuga de Clientes (Telco)")
    st.markdown("✅ **Objetivo:** Analizar y visualizar patrones asociados a la fuga de clientes (Churn) para mejorar la retención")
    st.markdown("✅ **Nombre Completo:** Gian Pier Giraldo Pariona")
    st.markdown("✅ **Curso / Especializacion:** Especializacion en Phyton for Analytics")
    st.markdown("✅ **Fecha:** Marzo 2026")
    st.markdown("---")

    st.markdown("✅ **Breve Explicación:** Durante esta especialización en Python for Analytics, logré comprender los principales parámetros y fundamentos para desarrollar aplicaciones utilizando Python. Aprendí a trabajar con diversas librerías y archivos de datos, que permiten extraer información y realizar operaciones para resolver problemas de manera eficiente. Asimismo, esta formación me permitió entender cómo optimizar el trabajo mediante el desarrollo de aplicaciones que automatizan procesos, mejorando la gestión y el análisis de información. Me siento muy satisfecho con la enseñanza del docente, quien explicó los contenidos de manera didáctica y práctica, utilizando ejemplos claros, lo que facilitó el aprendizaje y el uso de herramientas y librerías de Python aplicadas al análisis de datos")
    st.info("Este proyecto utiliza Python, Pandas, Matplotlib, Seaborn y Streamlit.")

# --- MÓDULO 2: CARGA DEL DATASET ---
elif modulo == "Carga de Datos":
    st.header("Módulo de Carga")
    archivo = st.file_uploader("Subir archivo TelcoCustomerChurn.csv", type=["csv"]) # [cite: 38]

    if archivo:
        df = pd.read_csv(archivo)
        st.session_state['df'] = df  # Guardamos en sesión para usarlo en otros módulos
        st.success("¡Archivo cargado correctamente! [cite: 38]")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Dimensiones:**")
            st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]} [cite: 39]")
        with col2:
            st.write("**Vista Previa:**")
            st.dataframe(df.head()) # [cite: 38]
    else:
        st.warning("Por favor, sube el archivo CSV para continuar[cite: 40].")

# --- MÓDULO 3: EDA (NÚCLEO) ---
elif modulo == "EDA":
    if 'df' not in st.session_state:
        st.error("Primero debes cargar los datos en el módulo 'Carga de Datos'[cite: 40].")
    else:
        df = st.session_state['df']
        analyzer = DataAnalyzer(df) # Instanciamos la clase
        
        tab1, tab2, tab3 = st.tabs(["Info General", "Estadísticas", "Visualización Dinámica"]) # [cite: 42, 95]

        with tab1:
            st.subheader("Información del Dataset")
            dtypes, nulls = analyzer.get_info()
            st.write("**Tipos de Datos y Nulos:**")
            info_df = pd.DataFrame({"Tipo": dtypes, "Nulos": nulls})
            st.table(info_df) # [cite: 45, 48]

        with tab2:
            st.subheader("Estadística Descriptiva")
            st.write(df.describe()) # [cite: 56, 57]
            
            num, cat = analyzer.classify_variables()
            st.write(f"**Variables Numéricas:** {len(num)}")
            st.write(f"**Variables Categóricas:** {len(cat)} [cite: 55]")

        with tab3:
            st.subheader("Análisis Visual Interactivo")
            # Selección dinámica [cite: 85, 87]
            opcion = st.selectbox("Selecciona una variable para analizar:", df.columns)
            
            if df[opcion].dtype in ['int64', 'float64']:
                st.pyplot(analyzer.plot_distribution(opcion)) # [cite: 68]
            else:
                st.pyplot(analyzer.plot_bivariate(opcion)) # [cite: 72, 74]

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    /* Imagen de fondo con una capa oscura para legibilidad */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), 
                    url("https://images.unsplash.com/photo-1557683316-973673baf926?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
    }
    
    /* Contenedor para el sticker movible */
    .sticker-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 100;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    </style>
    
    <div class="sticker-container">
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6NHJ4ZzR6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lTjJp8yYyG2bkc/giphy.gif" width="100">
    </div>
    """, unsafe_allow_html=True)



