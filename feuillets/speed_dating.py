import streamlit as st
import matplotlib.pyplot as plt
from fonctions import list_age, quality_o, quality_pf_o, nb_participant

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

df2 = df.groupby(['wave', 'dec', 'exphappy', 'gender', 'age', 'goal', 'attr2_1','shar2_1','sinc2_1','intel2_1','fun2_1','amb2_1'], dropna=False)['iid'].value_counts().reset_index()
df3 = df.groupby(['dec', 'exphappy', 'gender', 'age', 'goal', 'amb', 'attr', 'fun', 'intel', 'shar', 'sinc'], dropna=False)['iid'].value_counts().reset_index()

@st.cache_data
def pref_positive(df, age, decision):
    preference_positive = df[(df.dec == decision)]
    preference_positive = preference_positive.fillna(df.mean(numeric_only=True))
    research_good = preference_positive.groupby(['gender', (preference_positive.age == age)]).aggregate({'attr':'mean','sinc':'mean','intel':'mean','fun':'mean','amb':'mean','shar':'mean'}).reset_index()
    research_good = research_good[research_good.age == True]
    return research_good

st.markdown("## <font color='tomato'><ins>**SPEED DATING**</ins></font>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["##### :blue[***1. Qualités recherchées***]", "##### :blue[***2. qualités attribuées par hommes***]", "##### :blue[***3. qualités attribuées par les femmes***]", "##### :blue[***4. Sondage***]",])

# affichage qualités
with tab1:
    st.subheader("Qualités recherchées chez le sexe opposé lors de ce speed dating.")
    # qualité noteé dans les waves de 1 à 5 et de 10 à 21, les waves 6 à 9 sont non conformes à la notation demandée.
    # slider de selection de l'age
    age = st.select_slider("Selectionner l'age", options=list_age(df), key="attribution_bad1", value=25)
    st.write("L'age selectionné est ", age, "ans")
    wave1a5_10a21 = df2[(df2['wave'] <= 5) | (df2['wave'] >=10)]
    wave1a5_10a21 = wave1a5_10a21.fillna(df.mean(numeric_only=True))
    list_search = wave1a5_10a21.groupby(['gender', (wave1a5_10a21.age == age)]).aggregate({'attr2_1':'mean','shar2_1':'mean','sinc2_1':'mean','intel2_1':'mean','fun2_1':'mean','amb2_1':'mean'}).reset_index()
    list_search = list_search[list_search.age == True]    
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # Qualités recherchées par les femmes        
        list_search_female = list_search[list_search['gender'] == 0].reset_index()
        list_search_female = list_search_female.drop('gender', axis=1)
        list_search_female = list_search_female.drop('age', axis=1)        
        list_search_female = list_search_female.drop('index', axis=1)
        if list_search_female.empty:
            st.subheader("Pas de données féminine pour "+str(age)+ " ans")
        else:
            list_search_female.sort_values(ascending=True, by=0, axis=1, inplace=True)    
            list_search_female_label = list_search_female.columns.map(quality_o)        
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
            expander2.metric(value=df['attr2_1'][df.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes.")

    with col2:
        # Qualités recherchées par les hommes
        list_search_male = list_search[list_search['gender'] == 1].reset_index()
        list_search_male = list_search_male.drop('gender', axis=1)
        list_search_male = list_search_male.drop('age', axis=1)
        if list_search_male.empty: 
            st.subheader("Pas de données masculine pour "+str(age)+ " ans")
        else:
            list_search_male.sort_values(ascending=True, by=0, axis=1, inplace=True) 
            list_search_male_label = list_search_male.columns.map(quality_o)        
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
            expander2.metric(value=df['attr2_1'][df.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

#affichage qualités des hommes
with tab2:
    st.subheader("Attribution des qualités par les hommes suite au speed dating.")
    # slider de selection de l'age
    age = st.select_slider("Selectionner l'age", options=list_age(df), key="attribution_bad2", value=25)
    research_bad = pref_positive(df, age, 0)
    research_good = pref_positive(df, age, 1)
    # qualités attibuées sans suite de rdv
    st.write("L'age selectionné est ", age, "ans")
    col3, col4 = st.columns(2, gap='medium')
    with col3:
         # Attribution des qualités par les hommes        
        list_search_bad_male = research_bad[research_bad['gender'] == 1].reset_index()    
        list_search_bad_male = list_search_bad_male.drop('gender', axis=1)
        list_search_bad_male = list_search_bad_male.drop('age', axis=1)            
        list_search_bad_male = list_search_bad_male.drop('index', axis=1)        
        if list_search_bad_male.empty:
            st.subheader("Pas de données masculine pour "+str(age)+ " ans")
        else:
            list_search_bad_male.sort_values(ascending=True, by=0, axis=1, inplace=True)     
            list_search_bad_male_label = list_search_bad_male.columns.map(quality_pf_o)             
            list_search_bad_male = list_search_bad_male.squeeze()
            explode = list()
            explode.append(0.1)
            for i in range(len(list_search_bad_male)-1):
                explode.append(0)            
            fig1, ax1 = plt.subplots()
            st.subheader("Envers les femmes sans suite de rendez-vous")
            ax1.pie(list_search_bad_male, explode=explode, labels=list_search_bad_male_label,  autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
            ax1.axis('equal')
            st.pyplot(fig1, clear_figure=True)

    # qualités attibuées avec rdv
    with col4:
         # Attribution des qualités par les hommes         
        list_search_good_male = research_good[research_good['gender'] == 1].reset_index()    
        list_search_good_male = list_search_good_male.drop('gender', axis=1)
        list_search_good_male = list_search_good_male.drop('age', axis=1)            
        list_search_good_male = list_search_good_male.drop('index', axis=1)        
        if list_search_good_male.empty:
            st.subheader("Pas de données masculine pour "+str(age)+ " ans")
        else:
            list_search_good_male.sort_values(ascending=True, by=0, axis=1, inplace=True)     
            list_search_good_male_label = list_search_good_male.columns.map(quality_pf_o) 
            
            list_search_good_male = list_search_good_male.squeeze()
            explode = list()            
            for i in range(len(list_search_good_male)-1):
                explode.append(0)
            explode.append(0.1)            
            fig5, ax5 = plt.subplots()
            st.subheader("Envers les femmes avec rendez-vous")
            ax5.pie(list_search_good_male, explode=explode, labels=list_search_good_male_label,  autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
            ax5.axis('equal')
            st.pyplot(fig5, clear_figure=True)
    expander2 = tab2.expander("Valeurs manquantes :")
    expander2.metric(value=df['attr'][df.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

#affichage qualités des femmes
with tab3:
    st.subheader("Attribution des qualités par les femmes suite au speed dating.")
    # slider de selection de l'age
    age = st.select_slider("Selectionner l'age", options=list_age(df), key="attribution_bad3", value=25)
    research_bad_f = pref_positive(df, age, 0)
    research_good_f = pref_positive(df, age, 1)
    st.write("L'age selectionné est ", age, "ans")
    col5, col6 = st.columns(2, gap='medium')
    with col5:
        # Attribution des qualités par les femmes sans rendez-vous
        list_search_female = research_bad_f[research_bad_f['gender'] == 0].reset_index()
        list_search_female = list_search_female.drop('gender', axis=1)
        list_search_female = list_search_female.drop('age', axis=1)        
        list_search_female = list_search_female.drop('index', axis=1)
        if list_search_female.empty:
            st.subheader("Pas de données féminine pour "+str(age)+ " ans")
        else:
            list_search_female.sort_values(ascending=True, by=0, axis=1, inplace=True)     
            list_search_female_label = list_search_female.columns.map(quality_pf_o)        
            list_search_female = list_search_female.squeeze()
            explode = list()
            explode.append(0.1)
            for i in range(len(list_search_female)-1):
                explode.append(0)            
            fig6, ax6 = plt.subplots()
            st.subheader("Envers les hommes sans suite de rendez-vous")
            ax6.pie(list_search_female, explode=explode, labels=list_search_female_label,  autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
            ax6.axis('equal')
            st.pyplot(fig6, clear_figure=True)            

    with col6:
            # Attribution des qualités par les femmes avec rendez-vous
            list_search_female_good = research_good_f[research_good_f['gender'] == 0].reset_index()
            list_search_female_good = list_search_female_good.drop('gender', axis=1)
            list_search_female_good = list_search_female_good.drop('age', axis=1)        
            list_search_female_good = list_search_female_good.drop('index', axis=1)
            if list_search_female_good.empty:
                st.subheader("Pas de données féminine pour "+str(age)+ " ans")
            else:
                list_search_female_good.sort_values(ascending=True, by=0, axis=1, inplace=True)
                list_search_female_good_label = list_search_female_good.columns.map(quality_pf_o)        
                list_search_female_good = list_search_female_good.squeeze()
                explode = list()                
                for i in range(len(list_search_female_good)-1):
                    explode.append(0)
                explode.append(0.1)          
                fig2, ax2 = plt.subplots()
                st.subheader("Envers les hommes avec rendez-vous")
                ax2.pie(list_search_female_good, explode=explode, labels=list_search_female_good_label,  autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
                ax2.axis('equal')
                st.pyplot(fig2, clear_figure=True)

    expander2 = tab3.expander("Valeurs manquantes :")
    expander2.metric(value=df['attr'][df.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes.")

with tab4:
    df5 = df.groupby(['gender'])['satis_2'].mean().reset_index()
    sat_female = round(df5[df5.gender == 0].satis_2, 2)
    sat_male = round(df5[df5.gender == 1].satis_2, 2)
    df6 = df.groupby(['gender', 'length'])['iid'].value_counts().reset_index(name="iid_count")
    df6 = df6.groupby('gender')['length'].value_counts().reset_index()
    df8 = df6[df6.gender == 1]
    df7 = df6[df6.gender == 0]
    df9 = df.groupby(['gender', 'numdat_2'])['iid'].value_counts().reset_index(name="iid_count")
    df9 = df9.groupby('gender')['numdat_2'].value_counts().reset_index()
    df10 = df9[df9.gender == 1]
    df11 = df9[df9.gender == 0]
    container3 = st.container(border=True)    
    container3.write("Satisfaction sur les personnes rencontrées notée sur 10 :")

    col7, col8 = st.columns(2)
    with col7:
        st.metric(value=sat_male, label="Note pour les hommes")

    with col8:
        st.metric(value=sat_female, label="Note pour les femmes")
    container1 = st.container(border=True)    
    container1.write("Le temps imparti de 4 minutes du speed dating était :")
    col9, col10, col11 = st.columns(3)
    
    with col9:        
        st.metric(value=str(round((df8['count'][3])*100/nb_participant(df), 2)) + " %", label="trop peu pour les hommes")
        st.metric(value=str(round((df7['count'][0])*100/nb_participant(df), 2)) + " %", label="trop peu pour les femmes")       

    with col10:
        st.metric(value=str(round((df8['count'][4])*100/nb_participant(df), 2)) + " %", label="juste ce qu'il faut pour les hommes")
        st.metric(value=str(round((df7['count'][1])*100/nb_participant(df), 2)) + " %", label="juste ce qu'il faut pour les femmes")

    with col11:
        st.metric(value=str(round((df8['count'][5])*100/nb_participant(df), 2)) + " %", label="trop long pour les hommes")
        st.metric(value=str(round((df7['count'][2])*100/nb_participant(df), 2)) + " %", label="trop long pour les femmes")

    container2 = st.container(border=True)    
    container2.write("Le nombre de speed dating était :")
    col9, col10, col11 = st.columns(3)
    with col9:        
        st.metric(value=str(round((df10['count'][3])*100/nb_participant(df), 2)) + " %", label="trop peu pour les hommes")
        st.metric(value=str(round((df11['count'][0])*100/nb_participant(df), 2)) + " %", label="trop peu pour les femmes")       

    with col10:
        st.metric(value=str(round((df10['count'][4])*100/nb_participant(df), 2)) + " %", label="juste ce qu'il faut pour les hommes")
        st.metric(value=str(round((df11['count'][1])*100/nb_participant(df), 2)) + " %", label="juste ce qu'il faut pour les femmes")

    with col11:
        st.metric(value=str(round((df10['count'][5])*100/nb_participant(df), 2)) + " %", label="trop pour les hommes")
        st.metric(value=str(round((df11['count'][2])*100/nb_participant(df), 2)) + " %", label="trop pour les femmes")
    
txt = st.text_area(
    "#### **Interprétation :**",
    "Les qualités recherchées, en majorité par les hommes et les femmes avant les rendez-vous, sont l'attractivité. "
    "A l'issu de ces speed dating les qualités attribuées, que ce soit par les femmes ou les hommes, deviennent beaucoup plus équilibrées. "
    "On voit que rien ne permet clairement d'identifier pourquoi une suite est donnée avec un rendez-vous. "
    "L'indice de satisfaction des personnes rencontrées obtient à peine la moyenne, ce qui veut dire que les matchs proposés ne sont pas adéquates. "
    "Le temps de 4 minutes du speed dating en est peut-être la raison car trop court."
    ,)
st.divider()
expander = st.expander("considérations :")
expander.write("""Le speed dating est un rendez-vous d'une durée d'environ 4 mn avec le partenaire selectionné. Les valeurs manquantes ont été remplacées par la moyenne des valeurs."""
               """ Seul les waves 1 à 5 et de 10 à 21 ont été pris en considération, les autres waves n'étant pas conforme à la notation demandée.""")