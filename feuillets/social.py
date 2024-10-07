import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def student(x):
    if x == 1.0:
        size = "Law"
    elif x == 2.0:
        size = "Math"
    elif x == 3.0:
        size = "Social Science, Psychologist"
    elif x == 4.0:
        size = "Medical Science, Pharmaceuticals, and Bio Tech"
    elif x == 5.0:
        size = "Engineering"
    elif x == 6.0:
        size = "English/Creative Writing/ Journalism"
    elif x == 7.0:
        size = "History/Religion/Philosophy"
    elif x == 8.0:
        size = "Business/Econ/Finance"
    elif x == 9.0:
        size = "Education, Academia"
    elif x == 10.0:
        size = "Biological Sciences/Chemistry/Physics"
    elif x == 11.0:
        size = "Social Work"
    elif x == 12.0:
        size = "Undergrad/undecided"
    elif x == 13.0:
        size = "Political Science/International Affairs"
    elif x == 14.0:
        size = "Film"
    elif x == 15.0:
        size = "Fine Arts/Arts Administration"
    elif x == 16.0:
        size = "Languages"
    elif x == 17.0:
        size = "Architecture"
    else:
        size = "Other"
    return size

@st.cache_data
def ProfilSociaux(x):
    if x == 1.0:
        size = "Lawyer"
    elif x == 2.0:
        size = "Academic/Research"
    elif x == 3.0:
        size = "Psychologist"
    elif x == 4.0:
        size = "Doctor/Medicine"
    elif x == 5.0:
        size = "Engineer"
    elif x == 6.0:
        size = "Creative Arts/Entertainment"
    elif x == 7.0:
        size = "Banking/Consulting/Finance/Marketing/Business/CEO/Entrepreneur/Admin"
    elif x == 8.0:
        size = "Real Estate"
    elif x == 9.0:
        size = "International/Humanitarian Affairs"
    elif x == 10.0:
        size = "Undecided"
    elif x == 11.0:
        size = "Social Work"
    elif x == 12.0:
        size = "Speech Pathology"
    elif x == 13.0:
        size = "Politics"
    elif x == 14.0:
        size = "Pro sports/Athletics"
    elif x == 15.0:
        size = "Other"
    elif x == 16.0:
        size = "Journalism"
    elif x == 17.0:
        size = "Architecture"
    else:
        size = "Other"
    return size

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

df2 = df.groupby(['sports','tvsports','exercise','dining','museums','art', 'hiking','gaming','clubbing','reading','tv','theater','movies','music','shopping','yoga','concerts', 'gender', 'career_c', 'field_cd'], dropna=False)['iid'].value_counts().reset_index()

st.markdown("## <font color='tomato'><ins>**PROFIL SOCIAL**</ins></font>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["##### :blue[***1. Domaine des études***]", "##### :blue[***2. Professions***]", "##### :blue[***3. Hobbies***]"])

# domaine d'étude des hommes
etude = df2.groupby('field_cd', dropna=True)['gender'].value_counts().reset_index()
etude_male = etude[etude.gender == 1].set_index('field_cd')
etude_male = etude_male.drop('gender', axis=1)
etude_male = etude_male.squeeze()
other2 = etude_male[etude_male<etude_male.quantile(.50)].sum()
etude_male['others'] = other2
etude_male = etude_male[etude_male>=etude_male.quantile(.50)]
etude_male.index = etude_male.index.map(student)
etude_male.sort_values(ascending=True, inplace=True)
labels = etude_male.index
explode = list()
for i in range(len(etude_male)-1):
    explode.append(0)
explode.append(0.1)
fig1, ax1 = plt.subplots()
ax1.pie(etude_male, explode=explode, labels=labels, autopct="%0.0f%%", shadow=True, startangle=120, pctdistance=0.9)
ax1.axis('equal')

# domaine d'étude des femmes
etude_female = etude[etude.gender == 0].set_index('field_cd')
etude_female = etude_female.drop('gender', axis=1)
etude_female = etude_female.squeeze()
other2 = etude_female[etude_female<etude_female.quantile(.25)].sum()
etude_female['others'] = other2
etude_female = etude_female[etude_female>=etude_female.quantile(.25)]
etude_female.index = etude_female.index.map(student)
etude_female.sort_values(ascending=True, inplace=True)
labels = etude_female.index
explode = list()
for i in range(len(etude_female)-1):
    explode.append(0)
explode.append(0.1)
fig2, ax2 = plt.subplots()
ax2.pie(etude_female, explode=explode, labels=labels, autopct="%0.0f%%", shadow=True, startangle=120, pctdistance=0.9)
ax2.axis('equal')

# affichage des études
with tab1:
    col1, col2 = st.columns(2, gap='medium')
    with col1:        
        st.subheader("Domaine d'études masculin :")
        st.pyplot(fig1)
        expander6 = st.expander("Valeurs manquantes :")
        expander6.metric(value=df2['field_cd'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

    with col2:
        st.subheader("Domaine d'études féminin :")
        st.pyplot(fig2)
        expander7 = st.expander("Valeurs manquantes :")
        expander7.metric(value=df2['field_cd'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes.")

# professions
carriere = df2.groupby('career_c', dropna=True)['gender'].value_counts().reset_index()

# Profession des hommes
carriere_male = carriere[carriere.gender == 1].set_index('career_c')
carriere_male = carriere_male.drop('gender', axis=1)
carriere_male = carriere_male.squeeze()
other2 = carriere_male[carriere_male<carriere_male.quantile(.50)].sum()
carriere_male['others'] = other2
carriere_male = carriere_male[carriere_male>=carriere_male.quantile(.50)]
carriere_male.index = carriere_male.index.map(ProfilSociaux)
carriere_male.sort_values(ascending=True, inplace=True)
labels = carriere_male.index
explode = list()
for i in range(len(carriere_male)-1):
    explode.append(0)
explode.append(0.1)
fig3, ax3 = plt.subplots()
ax3.pie(carriere_male, explode=explode, labels=labels, autopct="%0.0f%%", shadow=True, startangle=180, pctdistance=0.8)
ax3.axis('equal')

# Profession des femmes
carriere_female = carriere[carriere.gender == 0].set_index('career_c')
carriere_female = carriere_female.drop('gender', axis=1)
carriere_female = carriere_female.squeeze()
other2 = carriere_female[carriere_female<carriere_female.quantile(.50)].sum()
carriere_female['others'] = other2
carriere_female = carriere_female[carriere_female>=carriere_female.quantile(.50)]
carriere_female.index = carriere_female.index.map(ProfilSociaux)
carriere_female.sort_values(ascending=True, inplace=True)
labels = carriere_female.index
explode = list()
for i in range(len(carriere_female)-1):
    explode.append(0)
explode.append(0.1)
fig4, ax4 = plt.subplots()
ax4.pie(carriere_female, explode=explode, labels=labels, autopct="%0.0f%%", shadow=True, startangle=180, pctdistance=0.8)
ax4.axis('equal')

# affichage des professions
with tab2:
    col3, col4 = st.columns(2, gap='medium')
    with col3:
        st.subheader("Métiers masculin :")
        st.pyplot(fig3)
        expander1 = st.expander("Valeurs manquantes :")
        expander1.metric(value=df2['career_c'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

    with col4:
        st.subheader("Métiers féminin :")
        st.pyplot(fig4)
        expander2 = st.expander("Valeurs manquantes :")
        expander2.metric(value=df2['career_c'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes.")

# Hobbies
hobbies = df2.groupby('gender', dropna=True).aggregate({'sports':'sum','tvsports':'sum','exercise':'sum','dining':'sum','museums':'sum','art':'sum', 'hiking':'sum','gaming':'sum','clubbing':'sum','reading':'sum','tv':'sum','theater':'sum','movies':'sum','music':'sum','shopping':'sum','yoga':'sum','concerts':'sum'})

# Hobbies des femmes
hobbies_female = hobbies.loc[hobbies.index == 0]
hobbies_female = hobbies_female.squeeze()
hobbies_female.sort_values(ascending=True, inplace=True)
colors = sns.color_palette("bright")
fig5, ax5 = plt.subplots()
ax5.pie(hobbies_female, labels=hobbies_female.index, autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
ax5.axis('equal')

# Hobbies des hommes
hobbies_male = hobbies.loc[hobbies.index == 1]
hobbies_male = hobbies_male.squeeze()
hobbies_male.sort_values(ascending=True, inplace=True)
colors = sns.color_palette("bright")
fig6, ax6 = plt.subplots()
ax6.pie(hobbies_male, labels=hobbies_male.index, autopct='%0.0f%%', shadow=True, startangle=90, pctdistance=0.7)
ax6.axis('equal')

with tab3:
    # affichage des hobbies
    col5, col6 = st.columns(2, gap='medium')
    with col5:
        st.subheader("Hobbies masculin :")
        st.pyplot(fig6)
        expander4 = st.expander("Valeurs manquantes :")
        expander4.metric(value=df2['movies'][df2.gender == 1].isnull().sum(), label="Nombre de valeurs manquantes.")

    with col6:
        st.subheader("Hobbies féminin :")
        st.pyplot(fig5)
        expander5 = st.expander("Valeurs manquantes :")
        expander5.metric(value=df2['movies'][df2.gender == 0].isnull().sum(), label="Nombre de valeurs manquantes.")