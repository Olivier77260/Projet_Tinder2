import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, f1_score, accuracy_score, recall_score, roc_auc_score, precision_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns

if st.session_state.del_from:
    df = st.session_state.dfTrue
else:
    df = st.session_state.dfFalse

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

@st.cache_data
def modele(df):
    features_list = ['age', 'fun', 'samerace', 'career_c', 'attr', 'gender' ]

    X = df.loc[:,features_list]
    y = df.loc[:,"dec"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    X_test = X_test.reset_index().drop(columns=["index"])
    X_test_age = X_test[X_test["attr"]==8]
    X_test_age.index.tolist()

    numeric_features = ['age', 'fun', 'samerace', 'attr', 'gender' ] # Choose which column index we are going to scale
    numeric_transformer = StandardScaler()

    categorical_features = ['career_c']
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", drop='first')

    # Apply ColumnTransformer to create a pipeline that will apply the above preprocessing
    feature_encoder = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features),    
            ('num', numeric_transformer, numeric_features)
            ]
        )

    X_train = feature_encoder.fit_transform(X_train)
    param_grid = {'C' : [0.01], 'solver' : ['saga']}
    # Initialiser le modèle de recherche de grille 
    regressor = GridSearchCV(LogisticRegression(), param_grid, cv=5) 
    # regressor = LogisticRegression()
    regressor.fit(X_train, y_train)
    y_train_pred = regressor.predict(X_train)
    X_test2 = feature_encoder.transform(X_test)
    y_test_pred = regressor.predict(X_test2)

    return X_train, y_train, X_test2, y_test, regressor, y_test_pred, feature_encoder, y_train_pred

@st.cache_data(persist=True)
def prepa_donnees(df):
    df_model = df[['age', 'fun', 'samerace', 'career_c', 'attr', 'gender', 'dec' ]]
    df_model = df_model.dropna()
    df_model.career_c = df_model.career_c.map(ProfilSociaux)   
    return df_model

df_modele = prepa_donnees(df)
mod_reg_logistique = modele(df_modele)
list_carrer = df_modele['career_c'].value_counts().reset_index()
# formulaire pour notre prédiction
with st.form("my_form"):
    st.write("Renseigner les élements ci-dessous")
    age = st.number_input("Votre age", min_value=18, max_value=55, format="%0.0f", step=1, placeholder="Type age...")
    career = st.selectbox(
        "Sélectionner votre profession",
        (list_carrer.career_c),
        index=None,
        placeholder="Select career...",
        )
    col1, col2, col3 = st.columns(3)
    with col1:
        genre = st.radio(
                "Quel est votre genre ?",
                ["0", "1"],
                captions=[
                    "Femme",
                    "Homme",
                ],
            )
    with col2:
        samerace = st.radio(
                "Es-ce important pour vous d'être de la même race ?",
                ["0", "1"],
                captions=[
                    "Non",
                    "Oui",
                ],
            )
    with col3:
        attractivite = st.slider("Es-ce important pour vous l'attractivité envers cette personne ?", 1, 10, 1)
        fun = st.slider("Es-ce important pour vous que cette personne soit fun ?", 1, 10, 1)
    submitted = st.form_submit_button("Submit")
    if submitted:
        data_dict = {"age":[age], "fun":[fun], "samerace":[samerace], "career_c":[career], "attr":[attractivite], "gender":[genre]}
        data_to_pred = pd.DataFrame(data_dict)
        st.write(data_to_pred)
        data_to_pred_encoded = mod_reg_logistique[6].transform(data_to_pred)
        pred = mod_reg_logistique[4].predict(data_to_pred_encoded)
        if pred[0] == 0:
            st.write("Les posibilités d'obtenir un rendez-vous sont faibles :umbrella_with_rain_drops:")
        else:
            st.success("Les posibilités d'obtenir un rendez-vous sont importantes", icon="🔥")

mse_test = mean_squared_error(mod_reg_logistique[3], mod_reg_logistique[5])
mse_train = mean_squared_error(mod_reg_logistique[1], mod_reg_logistique[7])

train_accurancy = accuracy_score(mod_reg_logistique[1], mod_reg_logistique[7])
test_accurancy = accuracy_score(mod_reg_logistique[3], mod_reg_logistique[5])

train_recall = recall_score(mod_reg_logistique[1], mod_reg_logistique[7])
test_recall = recall_score(mod_reg_logistique[3], mod_reg_logistique[5])

train_auc = roc_auc_score(mod_reg_logistique[1], mod_reg_logistique[7])
test_auc = roc_auc_score(mod_reg_logistique[3], mod_reg_logistique[5])

f1_score_train = f1_score(mod_reg_logistique[1], mod_reg_logistique[7])
f1_score_test = f1_score(mod_reg_logistique[3], mod_reg_logistique[5])

precision_train = precision_score(mod_reg_logistique[1], mod_reg_logistique[7])
precision_test = precision_score(mod_reg_logistique[3], mod_reg_logistique[5])


cm = confusion_matrix(mod_reg_logistique[1], mod_reg_logistique[7])
plt.figure(figsize=(4, 3), dpi=40)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Prédiction Négative', 'Prédiction Positive'],
            yticklabels=['Classe Négative', 'Classe Positive'])
plt.title('Matrice de Confusion')
plt.xlabel('Prédictions')
plt.ylabel('Valeurs Réelles')

performance_table = pd.DataFrame({
        'Métrique': ['Accuracy', 'Précision', 'Recall', 'F1_score', 'ROC AUC', 'MSE'],
        'Ensemble d\'entrainement': [train_accurancy, precision_train, train_recall, f1_score_train, train_auc, mse_train],
        'Ensemble de test': [test_accurancy, precision_test, test_recall, f1_score_test, test_auc, mse_test]
})

expander = st.expander("considérations :", icon="🚨")
expander.dataframe(performance_table)
expander.pyplot(plt, use_container_width=False)