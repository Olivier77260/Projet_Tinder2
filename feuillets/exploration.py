import streamlit as st
import matplotlib.pyplot as plt

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

@st.cache_data
def age_gender(genre, df):
    age_gender = df.groupby('age')['gender'].value_counts().reset_index(name='count')
    age_gender = age_gender.loc[age_gender['gender'] == genre]
    return age_gender

st.markdown("## <font color='tomato'><ins>**EXPLORATION DES DONNEES**</ins></font>", unsafe_allow_html=True)

# profil du fichier csv
col1, col2 = st.columns(2, gap="medium")
with col1:        
    st.metric(label="Nombre de lignes", value=df.shape[0])
with col2:
    st.metric(label="Nombre de colonnes", value=df.shape[1])

df_num = df.select_dtypes(exclude="object")
somme_num_value = df_num.columns.value_counts()
df_categories = df.select_dtypes(include="object")
somme_cat_value = df_categories.columns.value_counts()

col3, col4 = st.columns(2, gap="medium")
with col3:
    st.metric(label="Nombre de colonnes numérique", value=somme_num_value.sum())
with col4:
    st.metric(label="Nombre de colonnes catégorielles", value=somme_cat_value.sum())

st.divider()

# ages
st.write("#### Profil des âges masculins et féminins de nos participants")
age_gender_female = age_gender(0, df)
fig1, ax1 = plt.subplots()
ax1.set_ylabel('age')
ax1.set_title('Outlier des ages féminins')
ax1.boxplot(age_gender_female['age'], 0, 'gD', patch_artist=True, boxprops={'facecolor': 'bisque'}, widths=0.5)
# age_gender_male = age_gender.loc[age_gender['gender'] == 1]
age_gender_male = age_gender(1, df)
fig2, ax2 = plt.subplots()
ax2.set_ylabel('age')
ax2.set_title('Outlier des ages masculins')
ax2.boxplot(age_gender_male['age'], 0, 'gD', patch_artist=True, boxprops={'facecolor': 'bisque'}, widths=0.5)

col7, col8 = st.columns(2, gap="medium")
with col7:
    st.pyplot(fig1)
with col8:
    st.pyplot(fig2)

st.text_area(
    "#### **Interprétation :**",
    "Les données manquantes et abérantes seront supprimées à l'aide du bouton ci-contre.")