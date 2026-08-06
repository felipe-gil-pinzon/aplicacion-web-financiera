import streamlit as st
from pages.inicio import main
from pages.predecir import predecir
from pages.explorar  import explorar
     

if __name__ == "__main__":
     home_page = st.Page("pages/inicio.py", title="Inicio")
     prediction_page = st.Page("pages/predecir.py", title="Predecir")
     explore_page = st.Page("pages/explorar.py", title="Explorar")
     st.navigation({"Presentación": [home_page], "Predecciones con I.A":[prediction_page], "Acerca de Los Datos":[explore_page]}).run()
     