import streamlit as st
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer

st.markdown("## <font color='tomato'><ins>**DONNEES FOURNIES**</ins></font>", unsafe_allow_html=True)

st.subheader("Les informations fournies proviennent d'un fichier csv qui contient les données d'une étude faite suivant un panel de participants et un document explicatif sur cette base de données.")
st.subheader("Nom du dataframe : Speed_Dating_Data.csv")
st.subheader("Fichier descriptif : ")

if 'pdf_ref' not in ss:
    ss.pdf_ref = None

st.file_uploader("speed_dating_key.pdf", type=('pdf'), key='pdf')

if ss.pdf:
    ss.pdf_ref = ss.pdf

if ss.pdf_ref:
    binary_data = ss.pdf_ref.getvalue()
    pdf_viewer(input=binary_data, width=1000)