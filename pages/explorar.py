import streamlit as st

def explorar():
    if ("data" in st.session_state) and ("clientes" in st.session_state):
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
                        <h1>Modulo de exploración</h1>
                    </div>""", unsafe_allow_html=True)
        st.info("""En este modulo podras descargar y ver tus transacciones en
                        su totalidad""")

        data = st.session_state["data"]
        clientes = st.session_state["clientes"]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="section-card">
                            <h3>transacciones</h3></div>""", unsafe_allow_html=True)
            st.dataframe(data)
        with col2:
            st.markdown("""<div class="section-card">
                            <h3>clientes</h3></div>""", unsafe_allow_html=True)
            st.dataframe(clientes)

    else:
        st.error("No se ha detectado ninguna información transaccional")

if __name__ == "__main__":
    explorar()
else:
    explorar()