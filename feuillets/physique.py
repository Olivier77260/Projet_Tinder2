import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

@st.cache_data
def Races(x):
    if x == 1.0:
        size = "Black/African American"
    elif x == 2.0:
        size = "European/Caucasian-American"
    elif x == 3.0:
        size = "Latino/Hispanic American"
    elif x == 4.0:
        size = "Asian/Pacific Islander/Asian-American"
    elif x == 5.0:
        size = "Native American"
    else:
        size = "Other"
    return size

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

df2 = df.groupby(['age', 'gender', 'race'], dropna=False)['iid'].value_counts().reset_index()

adresses = pd.read_csv('adresses.csv', sep=';')

st.markdown("## <font color='tomato'><ins>**PROFIL PHYSIQUE**</ins></font>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["##### :blue[***1. Graphique des âges***]", "##### :blue[***2. Origines***]", "##### :blue[***3. Région du monde***]"])

#affichage des ages
with tab1:
    st.subheader("""Graphique des âges de nos participants :""")
    age_gender = df2.groupby('age')['gender'].value_counts().reset_index()
    age_gender['gender'] = age_gender['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')
    st.bar_chart(age_gender, x="age", y="count", color='gender', stack=False, use_container_width=True)
    expander1 = st.expander("Valeurs manquantes :")
    expander1.metric(value=df2['age'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes chez les femmes.")
    expander1.metric(value=df2['age'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes chez les hommes.")

# race féminine
race = df2.groupby('race', dropna=True)['gender'].value_counts().reset_index()
race.race = race.race.map(Races)
race_female = race[race.gender == 0]
race_female = race_female.drop('gender', axis=1)
race_female.sort_values('count', ascending=True, inplace=True)
color = sns.color_palette("bright")
explode = (0, 0, 0, 0, 0.1)
fig1, ax1 = plt.subplots()
ax1.pie(race_female['count'], explode=explode, labels=race_female.race, colors=color, autopct="%0.0f%%", shadow=True, startangle=-50)
ax1.axis('equal')

# race masculine
race_male = race[race.gender == 1]
race_male = race_male.drop('gender', axis=1)
race_male.sort_values('count', ascending=True, inplace=True)
explode = (0, 0, 0, 0, 0.1)
fig2, ax2 = plt.subplots()
ax2.pie(race_male['count'], explode=explode, labels=race_male.race, colors=color, autopct="%0.0f%%", shadow=True, startangle=-50)
ax2.axis('equal')

with tab2:
    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.subheader("Répartition de l'origine de la gente féminine :")
        st.pyplot(fig1)
        expander4 = st.expander("Valeurs manquantes :")
        expander4.metric(value=df2['race'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes chez les femmes.")
        
    with col2:
        st.subheader("Répartition de l'origine de la gente masculine :")
        st.pyplot(fig2)
        expander5 = st.expander("Valeurs manquantes :")
        expander5.metric(value=df2['race'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes chez les hommes.")

# carte du monde
with tab3:
    st.subheader("Carte du monde d'où viennet les participants.")
    st.map(adresses, latitude='latitude', longitude='longitude', zoom=1.5, color='#f20202', size='total')
