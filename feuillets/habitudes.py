import streamlit as st
from fonctions import list_age

@st.cache_data
def Frequence2(x):
    if x == 1:
        size = "1_Several times a week"
    elif x == 2:
        size = "2_Twice a week"
    elif x == 3:
        size = "3_Once a week"
    elif x == 4:
        size = "4_Twice a month"
    elif x == 5:
        size = "5_Once a month"
    elif x == 6:
        size = "6_Several times a year"
    else:
        size = "7_Almost never"
    return size

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

df2 = df.groupby(['go_out', 'gender', 'date', 'age', 'imprace', 'imprelig'], dropna=False)['iid'].value_counts().reset_index()

st.markdown("## <font color='tomato'><ins>**HABITUDES DE VIE DES PARTICIPANTS**</ins></font>", unsafe_allow_html=True)

# frequence des rendez-vous
sorties = df2.groupby('date', dropna=True)['gender'].value_counts().reset_index()
sorties['gender'] = sorties['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')
sorties.date = sorties.date.map(Frequence2)

# frequence des sorties
rdv = df2.groupby('go_out', dropna=True)['gender'].value_counts().reset_index()
rdv['gender'] = rdv['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')
rdv.go_out = rdv.go_out.map(Frequence2)

tab1, tab2, tab3 = st.tabs(["##### :blue[***1. Sorties et rendez-vous***]", "##### :blue[***2. Origines***]", "##### :blue[***3. Religions***]"])

# affichage des rdv et sorties
with tab1:
    col2, col3 = st.columns(2, gap='large')
    with col2:
        st.subheader("Fréquence des rendez-vous.")
        st.bar_chart(sorties, x='date', y='count', stack=False, y_label="Fréquence des rendez-vous", use_container_width=True, color="gender", horizontal=True)
        expander3 = st.expander("Valeurs manquantes :")      
        expander3.metric(value=df2['date'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes chez les femmes.")
        expander3.metric(value=df2['date'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes chez les hommes.")

    with col3:
        st.subheader("Fréquence des sorties.")        
        st.bar_chart(rdv, x='go_out', y='count', stack=False, y_label="Fréquence des sorties", use_container_width=True, color="gender", horizontal=True)
        expander4 = st.expander("Valeurs manquantes :")      
        expander4.metric(value=df2['go_out'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes chez les femmes.")
        expander4.metric(value=df2['go_out'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes chez les hommes.")

# affichage origine
with tab2:
    race = df2.groupby('imprace', dropna=True)['gender'].value_counts().reset_index()
    race['gender'] = race['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')
    race = race.drop(race[race.index==0].index)
    st.subheader("Importance des origines dans une relation :")
    st.bar_chart(race, x="imprace", y="count", x_label="Importance de l'origine", stack=True, use_container_width=True, color="gender")
    expander1 = st.expander("Valeurs manquantes :")      
    expander1.metric(value=df2['imprace'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes chez les femmes.")
    expander1.metric(value=df2['imprace'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes chez les hommes.")

# affichage religion
with tab3:
    religion = df2.groupby("imprelig", as_index=False)["gender"].value_counts()
    religion['gender'] = religion['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')
    st.subheader("Importance de la religion dans une relation.")
    st.bar_chart(religion, x="imprelig", y="count", stack=True, use_container_width=True, color="gender", x_label="Importance de la religion")
    expander2 = st.expander("Valeurs manquantes :")      
    expander2.metric(value=df2['imprelig'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes chez les femmes.")
    expander2.metric(value=df2['imprelig'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes chez les hommes.")