import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fonctions import nb_participant
from fonctions import list_age, quality_o_7_3, match

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

nb_rdv = match(df)

st.markdown("## <font color='tomato'><ins>**DEUXIEME RENDEZ-VOUS**</ins></font>", unsafe_allow_html=True)   

tab1, tab2, tab3 = st.tabs(["##### :blue[***1. Suivant l'âge***]", "##### :blue[***2. Suivant la race***]", "##### :blue[***2. Qualités recherchées***]"])

with tab1:
    st.subheader("Nombre de rendez-vous obtenu en fonction de l'âge.")  
    df1 = df.groupby(['age', 'gender', (df.date_3 == 1)])['num_in_3'].sum().reset_index()    
    df1['gender'] = df1['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')      
    st.bar_chart(df1, x="age", y="num_in_3", color='gender', y_label="total des rendez-vous", stack=False, use_container_width=True)
    expander2 = st.expander("Valeurs manquantes :")
    expander2.metric(value=df['num_in_3'][df.gender == 1][df.date_3 == 1].isnull().sum(), label="Pour les hommes.")
    expander2.metric(value=df['num_in_3'][df.gender == 0][df.date_3 == 1].isnull().sum(), label="Pour les femmes.")

with tab2:
    st.subheader("Nombre de rendez-vous obtenu entre des personnes de même race.")  
    df2 = df.groupby(['age', 'samerace', (df.date_3 == 1)])['num_in_3'].sum().reset_index()
    df2['samerace'] = df2['samerace'].apply(lambda x: 'Non' if x == 0 else 'Oui')
    st.bar_chart(df2, x="age", y="num_in_3", color='samerace', y_label="total des rendez-vous", stack=False, use_container_width=True)
    expander3 = st.expander("Valeurs manquantes :")
    expander3.metric(value=df['samerace'][df.gender == 1][df.date_3 == 1].isnull().sum(), label="Pour les hommes.")
    expander3.metric(value=df['samerace'][df.gender == 0][df.date_3 == 1].isnull().sum(), label="Pour les femmes.")

with tab3:    
    st.subheader("Aprés le rendez-vous, il a été demandé de repenser leurs décisions par rapport au speed dating.")
    age = st.select_slider("Selectionner l'age", options=list_age(df), key="attribution_bad", value=25)
    st.write("L'age selectionné est ", age, "ans")
    list_search = df.fillna(df.mean(numeric_only=True))
    list_search = list_search.groupby(['gender', (df.age == age), (df.date_3 == 1)], dropna=True).aggregate({'attr7_3':'mean','shar7_3':'mean','sinc7_3':'mean','intel7_3':'mean','fun7_3':'mean','amb7_3':'mean'}).reset_index()
    list_search = list_search[list_search.age == True]
    list_search = list_search[list_search.date_3 == True]
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # Qualités recherchées par les femmes
        if 0 not in list_search.values:
            st.subheader("Pas de données féminines pour "+str(age)+ " ans")
        else:
            list_search_female = list_search[list_search['gender'] == 0].reset_index()
            list_search_female = list_search_female.drop('gender', axis=1)
            list_search_female = list_search_female.drop('age', axis=1)
            list_search_female = list_search_female.drop('date_3', axis=1)
            list_search_female = list_search_female.drop('index', axis=1)  
            list_search_female.dropna(inplace=True)                   
            if list_search_female.empty:
                st.subheader("Pas de données féminines pour "+str(age)+ " ans")
            else:            
                list_search_female.sort_values(ascending=True, by=0, axis=1, inplace=True)            
                list_search_female_label = list_search_female.columns.map(quality_o_7_3)        
                list_search_female = list_search_female.squeeze()
                explode = list()
                for i in range(len(list_search_female)-1):
                    explode.append(0)
                explode.append(0.1)
                fig3, ax3 = plt.subplots()
                st.subheader("Envers les hommes")
                ax3.pie(list_search_female, explode=explode, labels=list_search_female_label,  autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
                ax3.axis('equal')
                st.pyplot(fig3)
                expander2 = st.expander("Valeurs manquantes :")
                expander2.metric(value=df['attr7_3'][df.gender == 0][df.date_3 == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

    with col2:
        # Qualités recherchées par les hommes
        if 1 not in list_search.values:
            st.subheader("Pas de données masculines pour "+str(age)+ " ans")
        else:
            list_search_male = list_search[list_search['gender'] == 1].reset_index()
            list_search_male = list_search_male.drop('gender', axis=1)
            list_search_male = list_search_male.drop('age', axis=1)
            list_search_male = list_search_male.drop('date_3', axis=1)
            list_search_male = list_search_male.drop('index', axis=1)
            list_search_male.dropna(inplace=True)                      
            if list_search_male.empty: 
                st.subheader("Pas de données masculine pour "+str(age)+ " ans")
            else:            
                list_search_male.sort_values(ascending=True, by=0, axis=1, inplace=True) 
                list_search_male_label = list_search_male.columns.map(quality_o_7_3)
                list_search_male = list_search_male.squeeze()        
                explode = list()
                for i in range(len(list_search_male)-1):
                    explode.append(0)
                explode.append(0.1)
                fig4, ax4 = plt.subplots()
                st.subheader("Envers les femmes")            
                ax4.pie(list_search_male, explode=explode, labels=list_search_male_label, autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
                ax4.axis('equal')
                st.pyplot(fig4)
                expander2 = st.expander("Valeurs manquantes :")
                expander2.metric(value=df['attr7_3'][df.gender == 1][df.date_3 == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.metric(value=nb_rdv, label="Nombre total de match suite au speed dating")

with col2:        
    total_rdv = df['num_in_3'][df.date_3 == 1].sum()
    st.metric(value=total_rdv, label="Nombre total de rendez-vous réellement obtenu")

with col3:
    pourcentage = np.round(total_rdv * 100 / nb_rdv, 2)
    st.metric(value=pourcentage, label="soit en pourcentage")

with col4:
    participant = nb_participant(df)
    pourcentage2 = np.round(total_rdv / participant, 2)
    st.metric(value=pourcentage2, label="Nombre de rendez-vous obtenu par participant")

txt = st.text_area(
    "#### **Interprétation :**",
    "Suite au nombre de personnes qui ont matché ensemble lors du speed dating, le nombre de rendez-vous obtenu aprés chute encore légérement . "
    "Nous avons en moyenne à peine un rendez-vous par personne, malgré une bonne correspondance dans les qualités recherchées. "
    "L'importance de la race dans une relation se retrouve bien ici dans les rendez-vous obtenus. "
    "La réévaluation de l'importance des qualités recherchées montre un changement de tendance vers l'attractivité. ",)

st.divider()
expander = st.expander("considérations :")
expander.write("Les valeurs manquantes ont été remplacées par la moyenne des valeurs.") 