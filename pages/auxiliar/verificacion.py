from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import pandas as pd
import numpy as np
import streamlit as st
import shap
from groq import Groq
from pathlib import Path



def transformar(data):
     data.drop(labels=["trans_num"], axis=1, inplace=True)

     cols = ["type_purcharse","gender","job"]
     or_cols = ["trans_month", "age_groups"]

     for or_col in or_cols:
          cod_or= OrdinalEncoder(categories=[data[or_col].unique()])
          data[or_col] = cod_or.fit_transform(data[[or_col]])


     for col in cols:
          encoder = OneHotEncoder()
          encoder_col = encoder.fit_transform(data[[col]])
          df_col = pd.DataFrame(encoder_col.toarray(), columns=encoder.categories_)
          data = pd.concat([data,df_col], axis=1)

     data.drop(labels=cols , axis=1, inplace=True)
     data.columns = [str(col[0]) if isinstance(col, tuple) else col for col in data.columns] 

     return data

def formato(columnas, data):
     BASE_DIR = Path(__file__).resolve().parent.parent.parent
     ruta_muestra = BASE_DIR / "data" / "muestra.csv"
     muestra = pd.read_csv(ruta_muestra)
     muestra.drop(labels=["fraud", "Unnamed: 0", "Unnamed: 0.1"], axis=1, inplace=True)
     orden = muestra.columns.tolist()
     valores = np.zeros(data.shape[0])

     for i in range(1, len(columnas)):
          col = columnas[i].strip()
          if col in muestra.columns:
               data[col] = valores
          else:
               return st.error("""
                          Al parecer, hay nuevas columnas o categorias dentro de estas transacciones,
                          se debe de reentrenar el modelo con estas nuevas categorias. Por favor,
                          contactese con su técnico""")

     data = data[orden]
     
     return data

def shap_global(shap_va, data):
     fraud = [] 
     valores = []

     for i in range(len(shap_va)):
          fraud.append(shap_va[i][:,1])

     for i in fraud:
          valores.append(i.values)

     base = shap_va.base_values

     test_array = data.values

     col_nombres = shap_va.feature_names

     fraud = shap.Explanation(values=valores,base_values=base,data=test_array, feature_names=col_nombres)
     return fraud

     valores = []

     for i in range(len(shap_va)):
          fraud.append(shap_va[i][:,1])

     for i in fraud:
          valores.append(i.values)

     features = shap_va.feature_names


     df_shap = pd.DataFrame({
     "feature": features,
     "shap_value": valores[0]})

     # Ordenar por impacto absoluto
     df_shap["abs_value"] = np.abs(df_shap["shap_value"])
     df_top5 = df_shap.sort_values("abs_value", ascending=False).head(5)

     df_top5 = df_top5.drop(columns="abs_value")

     if (len(transacciones) == 1) & (len(cliente) == 1):

          prompt =f"""Eres una I.A asistente para detectar fraude en tarjetas de credito,
                    a continuación se te entrega la siguient transacción
                    modelo: RandomoForest
                    nombre_cliente: {cliente["name"]}
                    numero_tarjeta: {cliente["cc_num"]}
                    transacción: {transacciones}
                    valores_shap: {df_top5}
                    Ten en cuenta que en los valores shap hay categorias de columnas
                    de la transacción hechas por onehotencoder, explica brevemente por que
                    esta transacción es o no fraudulenta""" 
     else:
          prompt= f"""Eres una I.A asistente para detectar fraude en tarjetas de credito
                    que va a explicar las desiciones del algoritmo RandomForest sobre
                    el siguiente conjunto de transacciones de diversos clientes:
                    monto_promedio: {transacciones["amount"].mean()}
                    grupo_etario_frecuente {transacciones["age_groups"].mode()}
                    trabajo_cliente_frecuente {transacciones["job"].mode()}
                    mes y año mas frecuente {transacciones["trans_month"].mode()},
                    {transacciones["trans_year"].mean()}
                    tipo de compra frecuente : {transacciones["type_purcharse"].mode()}
                    valores_shap: {df_top5}
                    Ten en cuenta que en los valores shap hay categorias de columnas
                    de la transacción hechas por onehotencoder, explica brevemente por que
                    este conjunto de transacciones es o no fraudulenta"""
     

     


def explicador_groq(shap_va, transacciones, cliente=[]):
     fraud = [] 
     valores = []

     for i in range(len(shap_va)):
          fraud.append(shap_va[i][:,1])

     for i in fraud:
          valores.append(i.values)

     features = shap_va.feature_names


     df_shap = pd.DataFrame({
     "feature": features,
     "shap_value": valores[0]})

     # Ordenar por impacto absoluto
     df_shap["abs_value"] = np.abs(df_shap["shap_value"])
     df_top5 = df_shap.sort_values("abs_value", ascending=False).head(5)

     df_top5 = df_top5.drop(columns="abs_value")

     if (len(transacciones) == 1) & (len(cliente) == 1):

          prompt =f"""
                    modelo: RandomoForest
                    nombre_cliente: {cliente["name"]}
                    numero_tarjeta: {cliente["cc_num"]}
                    transacción: {transacciones}
                    valores_shap: {df_top5}
                    Ten en cuenta que en los valores shap hay categorias de columnas
                    de la transacción hechas por onehotencoder""" 
     else:
          prompt= f"""
                    monto_promedio: {transacciones["amount"].mean()}
                    grupo_etario_frecuente {transacciones["age_groups"].mode()}
                    trabajo_cliente_frecuente {transacciones["job"].mode()}
                    mes y año mas frecuente {transacciones["trans_month"].mode()},
                    {transacciones["trans_year"].mean()}
                    tipo de compra frecuente : {transacciones["type_purcharse"].mode()}
                    valores_shap: {df_top5}
                    Ten en cuenta que en los valores shap hay categorias de columnas
                    de la transacción hechas por onehotencoder, explica brevemente por que
                    este conjunto de transacciones es o no fraudulenta"""
     

     
     client = Groq(api_key= st.secrets["CLAVE_API_GROQ"])

     completion = client.chat.completions.create(
          model="meta-llama/llama-4-scout-17b-16e-instruct",
          messages=[
               {
                    "role": "system",
                    "content": """Eres una i.a que explica las desiciones de un modelo RandomForest en 
                    detección de fraude de tarjetas de credito,cuando te den una sola transacción es referente
                    a un unico cliente, cuando sean varias, se refiere a varios clientes"""
               },
               {
                    "role": "user",
                    "content": f"{prompt}"
               }
               ],
          temperature=1,
          max_completion_tokens=1024,
          top_p=1,
          stream=True,
          stop=None
          )
     response = ""

     for chunk in completion:
          response += chunk.choices[0].delta.content or ""

     return response