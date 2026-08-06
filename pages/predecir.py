import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
from pages.models.modelo import Modelo
from joblib import load
from pages.auxiliar.verificacion import transformar, formato, shap_global, explicador_groq
import shap
from pathlib import Path


# Función para el apartado de predecir
def predecir():
#-------------------------------------------------------------------------------------------
# Titulko     
     st.markdown("""
     <style>
     .section-card {
     background-color: #2d6a76;
     padding: 25px;
     border-radius: 15px;
     margin-bottom: 20px;
     box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
     }
     .section-card h3 {
     margin-bottom: 10px;
     }
     </style>
     """, unsafe_allow_html=True)

     st.markdown("""<div class="section-card">
                    <h1>Modulo de predicción de fraude</h1></div>""", unsafe_allow_html=True)
# Subtitulo para cargar datos
     st.subheader("📂 Cargar Transacciones")
     
# Primer contenedor de carga
     with st.container(key="inicio"):

# cargar archivo csv
          archivo = st.file_uploader("Sube tu archivo CSV", type="csv")
          st.markdown('</div>', unsafe_allow_html=True)

          if archivo is not None:
          # cargar archivo en df y separar datos en cliente y transacción
               df = pd.read_csv(archivo)
               data = df[["trans_num","type_purcharse","amount","gender","job","trans_year","trans_month", "age_groups"]]
               clientes = df[["name", "age", "cc_num", "city", "trans_num", "state"]]
               st.session_state["data"] = data
               st.session_state["clientes"] = clientes

          # Contenedor de vista del df
               st.markdown("""<div class="section-card">
                    <h2>Vista general</h2></div>""", unsafe_allow_html=True)
               st.dataframe(df.head())

               with st.container(key="division"):
                    col1, col2 = st.columns(2)
                    with col1:
                         #info de las transacciones
                         st.markdown("""<div class="section-card">
                         <h3>Info transacciones</h3></div>""", unsafe_allow_html=True)
                         st.dataframe(data.head())
                    with col2:
                         # info de los clientes
                         st.markdown("""<div class="section-card">
                         <h3>Info clientes:</h3></div>""", unsafe_allow_html=True)
                         st.dataframe(clientes.head())

               st.text("""
                Perfecto, ahora que la información ha sido cargada exitosamente puedes continuar al siguiente apartado.
                Ten en cuenta que hemos hecho una división entre la información del cliente y la de la transacción.""")
               
          else:
               st.text("Una vez cargado las transacciones, se desplegara una vista general")

#-------------------------------------------------------------------------------------------
    
    # Segundo contenedor de procesamiento
     st.markdown("""<div class="section-card">
                    <h2>🗃️ Preprocesamiento</h2></div>""", unsafe_allow_html=True)
     st.text("""
             Para continuar exitosamente con el proceso debemos realizar una transformación 
             de las variables categoricas, oprime el boton transformar para llevar a cano el proceso.""")

     # Boton para transformar datos
     if st.button(key="transformar", label="⚙️ Transformar Datos", use_container_width=True):
          if "data" in st.session_state:
               # Guardar data en cache
               data_t= transformar(st.session_state["data"])
               st.success("El proceso se realizo exitosamente, puedes continuar al siguiente apartado")
               st.session_state["data_transformada"] = data_t
          else:
               st.error("Debes de importar primero las transacciones")

#-------------------------------------------------------------------------------------------
     
     # Titulo de predicciones
     st.markdown("""<div class="section-card">
                    <h2>🎱 Predicir</h2></div>""", unsafe_allow_html=True)
     st.text("""
             Por favor, haz click en el botón para realizar las predicciones,
             luego de esto podras revisar el informe de cada transacción.""")
       
     # Boton para prdecir fraude
     if st.button(key="predecir", label="🤖 Ejecutar Predicción", use_container_width=True):
        if "data_transformada" in st.session_state:
               try:
                  # Predecir fraude con RandomForest
                  BASE_DIR = Path(__file__).resolve().parent
                  ruta_modelo = BASE_DIR / "models" / "RandomForestClassifierHyper.joblib"
                  bh = load(ruta_modelo)
                  modelo = Modelo(bh)
                  
                  y_pred = modelo.predict(st.session_state["data_transformada"])
                  d = st.session_state["data"]
                  c = st.session_state["clientes"]
                  d["fraud"] = y_pred
                  c["fraud"] = y_pred
                  st.session_state["data_p"] = d
                  st.session_state["clientes_p"] = c
                  # Generar explicador shap
                  explicador = shap.Explainer(modelo.modelo)
                  st.session_state["explicador"] = explicador
                  st.success("El proceso se realizo exitosamente, puedes continuar al siguiente apartado")
               except ValueError as v:
                    # Excepción en caso de mal formato de datos
                    columnas = list(str(v).split(":")[-1].split("-"))
                    data_c = formato(columnas=columnas, data=st.session_state["data_transformada"])
                    y_pred= modelo.predict(data_c)
                    d = st.session_state["data"]
                    c = st.session_state["clientes"]
                    d["fraud"] = y_pred
                    c["fraud"] = y_pred
                    d["fraud"] = d["fraud"].replace(0,"no_fraude").replace(1,"fraude")
                    c["fraud"] = c["fraud"].replace(0,"no_fraude").replace(1,"fraude")
                    st.session_state["data_p"] = d
                    st.session_state["clientes_p"] = c
                    # Generar explicador shap
                    explicador = shap.Explainer(modelo.modelo)
                    st.session_state["explicador"] = explicador
                    st.success("El proceso se realizo exitosamente, puedes continuar al siguiente apartado")


        else:
               st.error("Debes de transformar las transacciones primero")

     # Titulo de reporte     
     st.markdown("""<div class="section-card">
                    <h2>📢 Reporte</h2></div>""", unsafe_allow_html=True)
     st.text("""
            filtra los datos por las características de tu interes y acontinuación
            recibiras un reporte del motivo de su categoria fraudulenta.""")
     
#-------------------------------------------------------------------------------------------

     # Tercer contenedor de reporte
     if "data_p" in st.session_state:
        with st.container(key="shap"):
             st.markdown("""<div class="section-card">
                    <h3>Por transacción y cliente</h3></div>""", unsafe_allow_html=True)
             opcion = st.selectbox("Selecciona el tipo de filtro", ["transaccion","clientes"])
             # Verificar por que filtrar transacciones (clientes o transaccion)
             if opcion == "transaccion":
                filtro = st.session_state["data_p"]
             else:
                filtro = st.session_state["clientes_p"]
            
             with st.container(key="transacción"):
                 # Elejir caracteristica y valor a filtrar
                 columna = st.selectbox(label="Seleccione la característica", options=filtro.columns)
                 llave = st.selectbox(label="¿Porque valor deseas filtrar?", options=filtro[columna].unique())
                 # Cuarto contenedor de graficas
                 if st.button(label="reporte", use_container_width=True):
                      if (columna is not None) & (llave is not None):
                           col1, col2 = st.columns(2)

                           # Caso de varias transacciones
                           if len(filtro[filtro[columna]==llave]) != 1:
                                with col1:
                                        # Generar grafico de pastel en la primera columna
                                        conteo = filtro[filtro[columna] == llave]["fraud"].value_counts()
                                        fig, ax = plt.subplots()
                                        ax.pie(conteo, labels=conteo.keys(), autopct="%1.1f%%")
                                        ax.set_title("Porcentaje de transacciones fraudulentas")
                                        st.pyplot(fig)
                                        try:
                                             st.text(f"se detectaron {conteo[1]} transacciones fraudulentas de un total de {conteo[0] + conteo[1]} transacciones")
                                        except:
                                             st.text(f"se detectaron {conteo[1]} transacciones de tipo {conteo.keys()[0]} de un total de {conteo[0]} transacciones")
                                
                                # Cargando explicador_shap, data transformada de referencia
                                explicador = st.session_state["explicador"]
                                data_t= st.session_state["data_transformada"]
                                # Mapeando los numeros de transacción a data transformada
                                data_t["trans_num"] = filtro["trans_num"]
                                # Seleccionando los numeros de transacción filtrados
                                ids = filtro[filtro[columna]==llave]["trans_num"]
                                # Mapeando los numeros de transacción deseados a data transformada
                                muestra = data_t[data_t["trans_num"].isin(ids)]
                                muestra.drop(labels=["trans_num"], axis=1, inplace=True)
                                
                                shap_va = explicador(muestra)

                                # Verificando que el filtro se encuentre en data_p
                                if filtro.equals(st.session_state["data_p"]):
                                   groq_data = filtro[filtro[columna]==llave]
                                   with col2:
                                        # Generar dataframe en la columna 2 con transacciones
                                        st.dataframe(groq_data)

                                else:
                                   # Cargando info de data_p en caso contrario
                                   data_p = st.session_state["data_p"]
                                   groq_data = data_p[data_p["trans_num"].isin(filtro[filtro[columna] == llave]["trans_num"])]
                                   with col2:
                                        # Generar dataframe en la columna 2 con transacciones
                                        st.dataframe(groq_data)
                               
                                try:
                                    # Genrando grafico shap
                                    fig,ax = plt.subplots()
                                    shap.plots.beeswarm(shap_va[:,:,1], max_display=10)
                                    plt.gcf().suptitle("Importancia de características")
                                    st.pyplot(plt.gcf())

                                    # Generando explicación textual
                                    response = explicador_groq(shap_va=shap_va, transacciones=groq_data)
                                    st.info(response)
                                    
                                except TypeError as t:
                                         st.error(f"Se detecto el siguiente error: {t}")
                               
                           # Caso de una única transacción    
                           else:
                                # verificando que filtro pertenezca a data_p
                                if filtro.equals(st.session_state["data_p"]):
                                    # Cargando información de clientes, explicador,ids de transacciones
                                    numero =  filtro[filtro[columna] == llave]["trans_num"].iloc[0]
                                    cliente = st.session_state["clientes_p"]
                                    data_t = st.session_state["data_transformada"]
                                    explicador = st.session_state["explicador"]
                                    # Mapeando  ids a data transformada 
                                    data_t["trans_num"] = filtro["trans_num"]
                                    transaccion = data_t[data_t["trans_num"] == numero]
                                    transaccion.drop(labels=["trans_num"], axis=1, inplace=True)

                                    try:
                                         # Cargando shap_values
                                         shap_va = explicador(transaccion)

                                         with col1:
                                             # Cargando info del cliente en columna 1
                                             st.markdown("""<div class="section-card">
                                                     <h3>Info del cliente</h3></div>""", unsafe_allow_html=True)
                                             st.dataframe(cliente[cliente["trans_num"]==numero])
                                    
                                         with col2:
                                             # Cargando info de la transacción en columna 2
                                             st.markdown("""<div class="section-card">
                                                       <h3>info transacciones</h3></div>""", unsafe_allow_html=True)
                                             st.dataframe(filtro[filtro[columna]==llave])

                                        # Generando grafico shap
                                         fig,ax = plt.subplots()
                                         shap.plots.waterfall(shap_va[0][:,1], max_display=10,show=False)
                                         plt.gcf().suptitle("Importancia de características")
                                         st.pyplot(plt.gcf())

                                        # Generando explicación textual
                                         groq_data = filtro[filtro[columna]==llave]
                                         groq_client = cliente[cliente["trans_num"]==numero]
                                         response = explicador_groq(shap_va=shap_va, transacciones=groq_data, cliente=groq_client)
                                     
                                         st.info(response)
                                    except ValueError as v:
                                         st.error(f"Se ha presentado el siguiente error: {v} al tratar de graficar")
                                    
                                   

                                # Mismo proceso en caso de que filtro este en clientes
                                else:
                                    data = st.session_state["data_p"]
                                    numero =  filtro[filtro[columna] == llave]["trans_num"].iloc[0]
                                    data_t = st.session_state["data_transformada"]
                                    explicador = st.session_state["explicador"]
                                    data_t["trans_num"] = filtro["trans_num"]
                                    transaccion = data_t[data_t["trans_num"] == numero]
                                    transaccion.drop(labels=["trans_num"], axis=1, inplace=True)
                                    try:
                                         shap_va = explicador(transaccion)
                                         with col1:
                                              st.markdown("""<div class="section-card">
                                                       <h3>info cliente</h3></div>""", unsafe_allow_html=True)
                                              st.dataframe(filtro[filtro[columna]==llave])
                                         with col2:
                                              st.markdown("""<div class="section-card">
                                                       <h3>info transacciones</h3></div>""", unsafe_allow_html=True)
                                              st.dataframe(data[data["trans_num"]==numero])
                                   
                                         fig,ax = plt.subplots()
                                         shap.plots.waterfall(shap_va[0][:,1], max_display=10,show=False)
                                         plt.gcf().suptitle("Importancia de características")
                                         st.pyplot(plt.gcf())

                                          
                                         groq_client = filtro[filtro[columna]==llave]
                                         groq_data = data[data["trans_num"]==numero]
                                         response =explicador_groq(shap_va=shap_va, transacciones=groq_data, cliente=groq_client)
                                         st.info(response)

                                    except ValueError as v:
                                         st.error(f"Se ha presentado el siguiente error: {v} al tratar de graficar")
                              
                                          
                                   
                      else:
                           st.warning("Primero completa el formulario")

if __name__ == "__main__":
     predecir()
else:
     predecir()