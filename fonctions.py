import streamlit as st
import pandas as pd

# Fonctions utilisées dans l'application avec leur mise en mémoire cache afin d'optimiser les resources.

# listing des âges
@st.cache_data
def list_age(df):
    list_age = df['age'].value_counts()
    list_age = list_age.index.sort_values(ascending=True)
    return list_age

# Calcul du nombre de participants en fonction de la selection faite
@st.cache_data
def nb_participant(df):
    if st.session_state.del_from:
        a = df['iid'].max()
        b = df.iid.value_counts().value_counts().sum()
        nb_participant = df['iid'].max() - (a-b)
        return nb_participant
    else:
        nb_participant = df['iid'].max()
        return nb_participant

# Calcul du nombre de personnes supprimées
@st.cache_data  
def delta(df):
    nb = nb_participant(df)
    delta = df['iid'].max() - nb
    return delta

# dataframe hors valeurs abérantes
@st.cache_data
def load_data_True():
    df = pd.read_csv("Speed_Dating_Data.csv", encoding="cp1252", sep=',')
    df.dropna(subset=['from', 'goal'], how='all', inplace=True)
    df =df[(df["age"] < 37) & (df["age"] > 18)].reset_index()
    df["diff_age"] = df["age_o"] - df["age"]
    return df

# dataframe complet
@st.cache_data
def load_data_False():
    df = pd.read_csv("Speed_Dating_Data.csv", encoding="cp1252", sep=',')
    df["diff_age"] = df["age_o"] - df["age"]
    return df

@st.cache_data
def quality_o(x):
    if x == 'attr2_1':
        size = "Attractive"
    elif x == 'sinc2_1':
        size = "Sincere"
    elif x == 'intel2_1':
        size = "Intelligent"
    elif x == 'fun2_1':
        size = "Fun"
    elif x == 'amb2_1':
        size = "Ambitious"
    else:
        size = "Has shared interests/hobbies"
    return size

@st.cache_data
def quality_pf_o(x):
    if x == 'attr':
        size = "Attractive"
    elif x == 'sinc':
        size = "Sincere"
    elif x == 'intel':
        size = "Intelligent"
    elif x == 'fun':
        size = "Fun"
    elif x == 'amb':
        size = "Ambitious"
    else:
        size = "Has shared interests/hobbies"
    return size

@st.cache_data
def quality_o_7(x):
    if x == 'attr7_2':
        size = "Attractive"
    elif x == 'sinc7_2':
        size = "Sincere"
    elif x == 'intel7_2':
        size = "Intelligent"
    elif x == 'fun7_2':
        size = "Fun"
    elif x == 'amb7_2':
        size = "Ambitious"
    else:
        size = "Has shared interests/hobbies"
    return size

@st.cache_data
def quality_o_7_3(x):
    if x == 'attr7_3':
        size = "Attractive"
    elif x == 'sinc7_3':
        size = "Sincere"
    elif x == 'intel7_3':
        size = "Intelligent"
    elif x == 'fun7_3':
        size = "Fun"
    elif x == 'amb7_3':
        size = "Ambitious"
    else:
        size = "Has shared interests/hobbies"
    return size

@st.cache_data
def load_data_rdv(df):
    df3 = df.groupby(['age', 'gender'])['match'].sum().reset_index()
    df3['gender'] = df3['gender'].apply(lambda x: 'Female' if x == 0 else 'Male')   
    return df3

@st.cache_data
def match(data1):
    df6 = load_data_rdv(data1)
    rdv = df6[df6.gender == 'Female'].sum()
    result = rdv.match
    return result