import streamlit as st
import pandas as pd
import pymongo

client = pymongo.MongoClient("mongodb+srv://CharlySimplon:1234@cluster0.vvomo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.datacars
cars_collection = db.collectioncars

data_cars = pd.DataFrame(list(cars_collection.find()))

# #HAUT DE PAGE
st.title("- Parc Automobile Simplon -")

#ACCROCHE + LOGO
st.subheader("Choisissez votre voiture de fonction...")

from PIL import Image 
img = Image.open("image.jpg") 
st.image(img, width=600) 

st.subheader("parmi les véhicules du parc automobile Simplon !")

#MASKS
mask_make_cars = mask_model_cars = mask_year_cars = pd.Series(True, index=data_cars.index)
choice = False

# #---NETTOYAGE---

# #NETTOYAGE LISTE UNIQUE

def removeduplicates(cars):
    cars_unique_list = []
    for car in cars:
        if car not in cars_unique_list:
            cars_unique_list.append(car)

    return cars_unique_list

#à remplacer par .unique() pour pandas OU .distinct() pour pymongo
# make_cars = [car for car in cars_collection.find().distinct('Make')]

#---SIDEBAR RECHERCHE---

st.sidebar.subheader("RECHERCHER UNE VOITURE")

#CRITERE CONSTRUCTEUR

if st.sidebar.checkbox('1. Constructeur'):
    make_cars = data_cars['Make'].sort_values()
    data_filtered = st.container()
    make_cars_choosen = st.sidebar.selectbox(
        'Constructeur : ',
        (removeduplicates(make_cars))
    )
    with data_filtered :
        mask_make_cars = data_cars['Make'].str.contains(make_cars_choosen)
        choice = True
    
    result_make_cars = data_cars[mask_make_cars]

#CRITERE MODELE
if st.sidebar.checkbox('2. Modèle de voiture'):
    if choice == False :
        st.sidebar.error("Veuillez choisir un constructeur")

    else:

        model_cars = result_make_cars['Model'].sort_values()
        data_filtered = st.container()
        model_cars_choosen = st.sidebar.selectbox(
            'Modèle de voiture recherché : ',
            (removeduplicates(model_cars)),
        )
        with data_filtered :
            mask_model_cars = data_cars['Model'].str.contains(model_cars_choosen)

    result_model_cars = data_cars[mask_make_cars & mask_model_cars]

# # CRITERE ANNEE
# if st.sidebar.checkbox('3. Année de la voiture'):
#     data_filtered = st.container()
#     year_cars_choosen = st.sidebar.number_input("Choisir l'année la plus ancienne acceptée :", min_value=1980, max_value=2021,value=2000, step=1)
#     with data_filtered :
#         mask_year_cars = data_cars['Year'] >= year_cars_choosen


#BOUTTON DE RECHERCHE
if st.sidebar.button('Recherchez ma voiture !'):

    result_cars = data_cars[mask_make_cars & mask_model_cars & mask_year_cars]
    def sentence():
        list_make = []
        list_model = []
        list_year = []
        list_horses = []
        list_cylinders = []
        list_highway = []
        list_city = []
        st.success("RESULTAT - Voici la liste des voitures concernées :")
        for x in range (0,len(result_cars)) :
            for car in result_cars['Make']:
                list_make.append(car)
            for car in result_cars['Model']:
                list_model.append(car)
            for car in result_cars['Year']:
                list_year.append(car)
            for car in result_cars['Engine HP']:
                list_horses.append(car)
            for car in result_cars['Engine Cylinders']:
                list_cylinders.append(car)
            for car in result_cars['Highway L/100km']:
                list_highway.append(car)
            for car in result_cars['City L/100km']:
                list_city.append(car)
            st.write(f" - La {list_make[x]} {list_model[x]} de {list_year[x]} a {list_horses[x]} chevaux et {list_cylinders[x]} cylindres.")
            st.write(f"Sa consommation sur autoroute est de {round(list_highway[x])} L au 100km et de {round(list_city[x])} L au 100km en ville.")

    sentence()

#---SIDEBAR AJOUT---

st.sidebar.subheader("AJOUTER UNE VOITURE")
#AJOUTER UNE VOITURE 

# nb_id = cars_collection.count_documents({})
# new_id = nb_id + 1
new_make = st.sidebar.text_input('Constructeur :')
new_model = st.sidebar.text_input('Modèle :')
new_year = st.sidebar.text_input('Année :')
new_engine_hp = st.sidebar.text_input('Chevaux :')
new_engine_c = st.sidebar.text_input('Cylindres :')


if st.sidebar.button('Ajoutez une voiture !'):
    cars_collection.insert_one({'Make': new_make, 'Model': new_model, 'Year': new_year, 'Engine HP': new_engine_hp, 'Engine Cylinders': new_engine_c })
