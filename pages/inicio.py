import streamlit as st

def main():
    st.set_page_config(page_title="Detección De Fraude", page_icon="💳")

    st.markdown("""
    <style>
    .hero {
        padding: 40px;
        border-radius: 15px;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        text-align: center;
    }
    .hero h1 {
        font-size: 42px;
        margin-bottom: 10px;
    }
    .hero p {
        font-size: 18px;
        opacity: 0.85;
    }
    </style>

    <div class="hero">
        <h1>🛡 Sistema Inteligente de Detección de Fraude</h1>
        <p>Simulación de uso de I.A para la deteccion de fraude crediticio</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .card {
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        background-color: #0A3D62;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .card h3 {
        margin-bottom: 10px;
    }
    </style>
                
    <div class="card">
        <h3>🙋🏻‍♂️ Presentación</h3>
        <p>La siguiente aplicación web es el resultado de una propuesta de investigación que tiene
           como objetivo dar cuenta de la utilidad practica que puede tener el modelo de I.A ante la
           problematica.</p>
    </div>
                
    <div class="card">
        <h3>🤖 Modelo de I.A</h3>
        <p>El modelo está basado en el algoritmo de machine learning Random Forest</p>
        <h4> Ventajas </h4>
        <ul>
            <li>Presico y estable para la problmática dada</li>
            <li>Buena adaptabilidad hacia nuevas transacciones</li>
            <li>Ideal para manejar muvhas transacciones</li>    
        </ul>
        <h4>Desventajas</h4>
            <ul>
                <li> Requiere de muchos recursos computacionales</li>
           </ul>
    </div>

    <div class="card">
        <h3>📊 Variables Analizadas</h3>
        <ul>
            <li>Monto de la transacción</li>
            <li>Tipo de compra</li>
            <li>Género del cliente</li>
            <li>Trabajo del cliente</li>
            <li>Residencia del cliente</li>
            <li>Fecha de la transacción</li>
            <li>Número de tarjeta</li>
            <li>Edad del cliente</li>
        </ul>
    </div>
                
    <div class="card">
    <h3>🔎 ¿Qué hace el sistema?</h3>
    <ul>
        <li>Detecta patrones anómalos</li>
        <li>Clasifica transacciones por lotes entre las categorías fraude y no_fraude</li>
        <li>Permite filtrar transacciones por información de la misma o del cliente</li>
        <li>Genera graficos estadísticos y explicativos</li>
        <li>Hace explicaciones textuales</li>
    </div>
    """, unsafe_allow_html=True)





    
if __name__ == "__main__":
    main()
else:
    main()