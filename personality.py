#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:10:43 2024

@author: deni-kun
"""

import streamlit as st
import os
import datetime
import requests

#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText

# Define your result_filename and global_results_filename
result_filename = "results.txt"
global_results_filename = "global_results.txt"
icon = "Favicon_2x.ico"

#post to database
DATABASE_URL = st.secrets["DATABASE_URL"]
DATABASE_API_KEY = st.secrets["DATABASE_API_KEY"]

def post_results_to_database(user, orga, A_score, B_score, C_score, D_score):
    url = f"{DATABASE_URL}/rest/v1/hermann_teams"
    headers = {
        "apikey": DATABASE_API_KEY,
        "Authorization": f"Bearer {DATABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    data = {
        "user": user,
        "organisation": orga,
        "A_score": A_score,
        "B_score": B_score,
        "C_score": C_score,
        "D_score": D_score
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# Function to append results to the global_results.txt file
def append_to_global_results(timestamp, user, orga, A_score, B_score, C_score, D_score):
    with open(global_results_filename, 'a') as global_results_file:
        global_results_file.write(f"{timestamp} - {user} - {orga} - A: {A_score}, B: {B_score}, C: {C_score}, D: {D_score}\n")

# Check if the global_results.txt file exists, if not, create it
if not os.path.exists(global_results_filename):
    with open(global_results_filename, 'w') as global_results_file:
        global_results_file.write("Timestamp - user - orga - A Score, B Score, C Score, D Score\n")



def create_result_text_file(filename, user, orga, personality_scores, coef):
    with open(filename, 'w') as file:
        file.write("Your results are :\n")
        file.write(f'user : {user}\n')
        file.write(f"organisation : {orga}\n")
        file.write(f"A_score = {coef * personality_scores.get('A')}\n")
        file.write(f"B_score = {coef * personality_scores.get('B')}\n")
        file.write(f"C_score = {coef * personality_scores.get('C')}\n")
        file.write(f"D_score = {coef * personality_scores.get('D')}\n")


st.set_page_config(layout='wide', page_icon=icon, page_title='Boussole des personnalités')

A_text = """L'ingénieur aime bien résoudre des problèmes en utilisant la méthode scientifique et le raisonnement logique. 
Il est dans la réflexion et est capable de conceptualiser des notions abstraites. C'est une personnalité plutôt introvertie qui aime analyser et savoir.\n
***Points de force*** : compilent les faits, analysent, argumentent rationnellement, formulent des théories, mesurent précisément, résolvent les problèmes logiquement, 
raisonnent, comprennent les éléments techniques, analysent avec l’esprit critique, travaillent à partir de chiffres, de statistiques, et sont précis."""

B_text = """Le cartographe est prudent et organisé. Il a des habitudes bien précises et respecte soigneusement les règles.
Il planifie méticuleusement ce qui doit être fait et se retrouve bien dans les tâches administratif ou son souci du détail est sa fiabilité est valorisé.\n
***Points de force*** : remarquent les défauts, approchent les problèmes pratiquement, vont jusqu’au bout des choses, développent des plans détaillés et des procédures, et envisagent les problèmes sous l’angle du planning."""

C_text = """Le barde aime le contact humain. Il est empathique, relationnel et amicale. Il est expressif et communique bien avec les autres.\n
***Points de force*** : comprennent les difficultés relationnelles, anticipent le ressenti des autres, comprennent intuitivement le ressenti des autres, perçoivent des éléments non verbaux issus du stress, engendrent l’enthousiasme, persuadent, concilient, enseignent, partagent, comprennent les éléments émotionnels, prennent en compte les valeurs."""

D_text = """L'inventeur est un aventurier avec une imagination débordante qui rêve éveillé. C'est un visionnaire qui a toujours des idées très originales.
C'est aussi un revel qui aime bien prendre des risuqes et se projeter.\n
***Points de force*** : Lisent les signes du changement, voient les choses globalement, reconnaissent les nouvelles possibilités, tolèrent l’ambiguïté, intègrent les idées et les concepts, défient les règles établies, synthétisent les éléments divers en un nouveau tout, inventent des solutions nouvelles, résolvent les problèmes de manière intuitive, intègrent en simultané différents inputs."""

st.image('Banniere argios.png', use_column_width=True)
st.title('Boussole des personalités')
user = st.text_input('Renseignez pseudo', placeholder='Votre pseudo ici')
orga = st.text_input("Renseignez l'id du test", placeholder="L'id qu'on vous a fourni pour ce test")

personality_scores = {
    'A':0,
    'B':0,
    'C':0,
    'D':0
    }

st.header('Activités de Travail')

st.write("Parmis les activités ci-dessous, cochez celles que vous faites bien, ou très bien")

col1, col2 = st.columns(2)
with col1:
    activites= {
        'analyser':st.checkbox('Analyser'),
        'administrer':st.checkbox('Administrer'),
        'conceptualiser':st.checkbox('Conceptualiser'),
        'exprimer':st.checkbox('Exprimer des idées'),
        'synth':st.checkbox('Synthétiser'),
        'orga':st.checkbox('Organiser'),
        'rationaliser':st.checkbox('Rationaliser'),
        'concretiser':st.checkbox('Concrétiser')
        }
with col2:
    activites2={
        'echanger':st.checkbox('Échanger (contact)'),
        'problem_solve':st.checkbox('Résoudre des problèmes'),
        'innov':st.checkbox('Innover'),
        'former':st.checkbox('Enseigner/former'),
        'create':st.checkbox('Créer'),
        'chiffre':st.checkbox('Chiffrer/calculer'),
        'planifie':st.checkbox('Planifier'),
        'animer':st.checkbox('Animer (réunion)')        
        }

if activites['analyser']:
    personality_scores['A'] +=1
if activites['administrer']:
    personality_scores['B'] +=1
if activites['conceptualiser']:
    personality_scores['D']+=1
if activites['exprimer']:
    personality_scores['C'] +=1
if activites['synth']:
    personality_scores['D'] +=1
if activites['orga']:
    personality_scores['B'] +=1
if activites['rationaliser']:
    personality_scores['A'] +=1
if activites['concretiser']:
    personality_scores['B'] +=1
if activites2['echanger']:
    personality_scores['C'] +=1
if activites2['problem_solve']:
    personality_scores['A'] +=1
if activites2['innov']:
    personality_scores['D'] +=1
if activites2['former']:
    personality_scores['C'] +=1
if activites2['create']:
    personality_scores['D'] +=1
if activites2['chiffre']:
    personality_scores['A'] +=1
if activites2['planifie']:
    personality_scores['B'] +=1
if activites2['animer']:
    personality_scores['C'] +=1

st.header('Mots clés')

st.write("Dans la liste ci-dessous, sélectionnez 10 adjectifs qui vous caractérisent le mieux")

col1, col2 = st.columns(2)
with col1:
    mots_cles = {
        'Logique':st.checkbox('Logique'),
        'Seviable':st.checkbox('Serviable'),
        'Organisé':st.checkbox('Organisé'),
        'Confiant':st.checkbox('Confiant'),
        'Rationnel':st.checkbox('Rationnel'),
        'Conservateur':st.checkbox('Conservateur'),
        'Expressif':st.checkbox('Expressif'),
        'Analytique':st.checkbox('Analytique'),
        'Émotif':st.checkbox('Émotif'),
        'Lecteur technique':st.checkbox('Lecteur technique'),
        'Réaliste':st.checkbox('Réaliste'),
        'Créatif':st.checkbox('Créatif'),
        'Intuitif : sentiments':st.checkbox('Intuitif : sentiments'),
        'Passionné':st.checkbox('Passionné'),
        'Critique':st.checkbox('Critique'),
        'Amical':st.checkbox('Amical'),
        'Objectif':st.checkbox('Objectif'),
        'Imaginatif':st.checkbox('Imaginatif'),
        'Coopératif':st.checkbox('Coopératif'),
        'Enthousiaste':st.checkbox('Enthousiaste'),
        'Pondéré':st.checkbox('Pondéré')
        }
with col2:
    mots_cles2 = {
        'Artistique':st.checkbox('Artistique'),
        'Souple':st.checkbox('Souple'),
        'Discret':st.checkbox('Discret'),
        'Précis':st.checkbox('Précis'),
        'Contrôlé':st.checkbox('Contrôlé'),
        'Sérieux':st.checkbox('Sérieux'),
        'Tenace':st.checkbox('Tenace'),
        'Minutieux':st.checkbox('Minutieux'),
        'Intuitif : Solutions':st.checkbox('Intuitif : Solutions'),
        'Simultané':st.checkbox('Simultané'),
        'Compétiteur':st.checkbox('Compétiteur'),
        'Aventurier':st.checkbox('Aventurier'),
        'Ordinné':st.checkbox('Ordonné'),
        'Libéral':st.checkbox('Libéral'),
        'Discipliné':st.checkbox('Discipliné'),
        'Curieux':st.checkbox('Curieux'),
        'Conventionnel':st.checkbox('Conventionnel'),
        'Original':st.checkbox('Original'),
        'Indépendant':st.checkbox('Indépendant')
        }

selected_mots = sum(mots_cles.values())+sum(mots_cles2.values())
st.write(f'Vous avez sélectionné {selected_mots} mots clés')

if selected_mots > 10:
    st.error('Vous ne pouvez selectionner que 10 mots clés', icon='😢')

if mots_cles['Logique']:
    personality_scores['A'] +=1
    
if mots_cles['Seviable']:
    personality_scores['C'] +=1

if mots_cles['Organisé']:
    personality_scores['B'] +=1

if mots_cles['Confiant']:
    personality_scores['C'] +=1

if mots_cles['Rationnel']:
    personality_scores['A'] +=1

if mots_cles['Conservateur']:
    personality_scores['B'] +=1

if mots_cles['Expressif']:
    personality_scores['C'] +=1

if mots_cles['Analytique']:
    personality_scores['A'] +=1

if mots_cles['Émotif']:
    personality_scores['C'] +=1

if mots_cles['Lecteur technique']:
    personality_scores['B'] +=1

if mots_cles['Réaliste']:
    personality_scores['A'] +=1

if mots_cles['Créatif']:
    personality_scores['D'] +=1

if mots_cles['Intuitif : sentiments']:
    personality_scores['C'] +=1

if mots_cles['Passionné']:
    personality_scores['C'] +=1

if mots_cles['Critique']:
    personality_scores['A'] +=1

if mots_cles['Amical']:
    personality_scores['C'] +=1

if mots_cles['Objectif']:
    personality_scores['A'] +=1

if mots_cles['Imaginatif']:
    personality_scores['D'] +=1

if mots_cles['Coopératif']:
    personality_scores['C'] +=1

if mots_cles['Enthousiaste']:
    personality_scores['C'] +=1

if mots_cles['Pondéré']:
    personality_scores['A'] +=1

if mots_cles2['Artistique']:
    personality_scores['D'] +=1

if mots_cles2['Souple']:
    personality_scores['C'] +=1

if mots_cles2['Discret']:
    personality_scores['A'] +=1

if mots_cles2['Précis']:
    personality_scores['A'] +=1

if mots_cles2['Contrôlé']:
    personality_scores['B'] +=1

if mots_cles2['Sérieux']:
    personality_scores['A'] +=1

if mots_cles2['Tenace']:
    personality_scores['B'] +=1

if mots_cles2['Minutieux']:
    personality_scores['B'] +=1

if mots_cles2['Intuitif : Solutions']:
    personality_scores['D'] +=1

if mots_cles2['Simultané']:
    personality_scores['D'] +=1

if mots_cles2['Compétiteur']:
    personality_scores['B'] +=1

if mots_cles2['Aventurier']:
    personality_scores['D'] +=1

if mots_cles2['Ordinné']:
    personality_scores['B'] +=1

if mots_cles2['Libéral']:
    personality_scores['D'] +=1

if mots_cles2['Discipliné']:
    personality_scores['B'] +=1

if mots_cles2['Curieux']:
    personality_scores['D'] +=1

if mots_cles2['Conventionnel']:
    personality_scores['B'] +=1

if mots_cles2['Original']:
    personality_scores['D'] +=1

if mots_cles2['Indépendant']:
    personality_scores['D'] +=1

st.header('Loisirs')

st.write('Selectionnez les loisirs que vous pratiquez ou que vous aimeriez pratiquer')

col1, col2 = st.columns(2)

with col1:
    loisirs = {
        'photo': st.checkbox('Photographie'),
        'farniente': st.checkbox('Farniente'),
        'radioamateur': st.checkbox('Radioamateur'),
        'chasse': st.checkbox('Chasse'),
        'peche': st.checkbox('Pêche'),
        'jadinage': st.checkbox('Jardinage'),
        'travail_bois':st.checkbox('Travail du bois'),
        'musique': st.checkbox('Musique'),
        'jogging':st.checkbox('Jogging'),
        'repare_voiture':st.checkbox('Réparation de voitures'),
        'chant':st.checkbox('Chant'),
        'benevolat':st.checkbox('Bénévolat'),
        'lecture':st.checkbox('Lecture'),
        'bricolage':st.checkbox('Bricolage'),
        'spect_sport':st.checkbox('Spectateur sportif'),
        'collect':st.checkbox('Collections')
        }
with col2:
    loisirs2 = {
        'jeux_hasard':st.checkbox('Jeux de hasard'),
        'artisanats':st.checkbox('Artisanats'),
        'cuisine':st.checkbox('Cuisine'),
        'conversations':st.checkbox('Conversations'),
        'théâtre':st.checkbox('Théâtre'),
        'jeux_cartes':st.checkbox('Jeux de cartes'),
        'peche_ss_marine':st.checkbox('Pêche sous marine'),
        'voyages':st.checkbox('Voyages'),
        'botanique':st.checkbox('Botanique'),
        'golf':st.checkbox('Golf'),
        'ordinateur':st.checkbox('Ordinateur'),
        'danse':st.checkbox('Danse'),
        'jeux_strat':st.checkbox('Jeux de stratégie'),
        'jeux_logik':st.checkbox('Jeux de logique'),
        'jeux_societe':st.checkbox('Jeux de société'),
        'bowling':st.checkbox('Bowling') 
        }
    
if loisirs["photo"]:
    personality_scores["D"] += 1

if loisirs['farniente']:
    personality_scores["D"] += 1

if loisirs['radioamateur']:
    personality_scores["A"] += 1

if loisirs['chasse']:
    personality_scores["A"] += 1

if loisirs['peche']:
    personality_scores["B"] += 1

if loisirs['jadinage']:
    personality_scores['C'] +=1
    
if loisirs['travail_bois']:
    personality_scores['A'] +=1
    
if loisirs['musique']:
    personality_scores['C'] +=1

if loisirs['jogging']:
    personality_scores['B'] +=1

if loisirs['repare_voiture']:
    personality_scores['A'] +=1

if loisirs['chant']:
    personality_scores['C'] +=1

if loisirs['benevolat']:
    personality_scores['C'] +=1

if loisirs['lecture']:
    personality_scores['C'] +=1

if loisirs['bricolage']:
    personality_scores['A'] +=1

if loisirs['spect_sport']:
    personality_scores['B'] +=1

if loisirs['collect']:
    personality_scores['B'] +=1

if loisirs2['jeux_hasard']:
    personality_scores['D'] +=1

if loisirs2['artisanats']:
    personality_scores['D'] +=1

if loisirs2['cuisine']:
    personality_scores['B'] +=1

if loisirs2['conversations']:
    personality_scores['C'] +=1

if loisirs2['théâtre']:
    personality_scores['D'] +=1

if loisirs2['jeux_cartes']:
    personality_scores['B'] +=1

if loisirs2['peche_ss_marine']:
    personality_scores['D'] +=1

if loisirs2['voyages']:
    personality_scores['C'] +=1

if loisirs2['botanique']:
    personality_scores['B'] +=1

if loisirs2['golf']:
    personality_scores['A'] +=1

if loisirs2['ordinateur']:
    personality_scores['A'] +=1

if loisirs2['danse']:
    personality_scores['D'] +=1

if loisirs2['jeux_strat']:
    personality_scores['D'] +=1

if loisirs2['jeux_logik']:
    personality_scores['A'] +=1

if loisirs2['jeux_societe']:
    personality_scores['C'] +=1

if loisirs2['bowling']:
    personality_scores['B'] +=1


st.header('20 Questions')
st.write('Sélectionnez les activités que vous aimez ou aimeriez pratiquer.')

col1, col2 = st.columns(2)
with col1:
    questions = {
        'Pratiquer des jeux de logique':st.checkbox('Pratiquer des jeux de logique'),
        'Dresser un arbre généalogique':st.checkbox('Dresser un arbre généalogique'),
        'Prendre la voiture ou le vélo et rouler sans but':st.checkbox('Prendre la voiture ou le vélo et rouler sans but'),
        'Construire':st.checkbox("Construire un article en kit en suivant la notice d'assemblage"),
        'Jouer avec des enfants':st.checkbox('Jouer avec des enfants'),
        'Rêver éveillé':st.checkbox('Rêver éveillé'),
        'Créer des logos':st.checkbox('Créer des logos'),
        'Ordre':st.checkbox("Mettre de l'ordre dans les photographies"),
        'Sortir':st.checkbox('Sortir avec des amis et faire la fête'),
        'Cerf':st.checkbox('Faire voler un cerf-volant')
        }
with col2:
    questions2 ={
        'Plat':st.checkbox('Préparer un plat de votre invention'),
        'Ordi':st.checkbox('Faire fonctionner (ou apprendre à faire fonctionner) un ordinateur'),
        'Réparer':st.checkbox("Réparer les pannes des machines ou des appareils"),
        'Écouter de la musique':st.checkbox('Écouter de la musique'),
        'Coquilles':st.checkbox('Repérer des coquilles dans un livre ou des erreurs sur un relevé bancaire'),
        'Ressentir une émotion devant un paysage, un tableau ou une scène':st.checkbox('Ressentir une émotion devant un paysage, un tableau ou une scène'),
        'Bourse':st.checkbox("Adhérer à un club d'investissement en Bourse"),
        'Connard':st.checkbox("Jouer à l'avocat du diable dans une discussion"),
        'Club':st.checkbox('Animer un cercle ou un club'),
        'Pratiquer le modélisme':st.checkbox('Pratiquer le modélisme')
        }

if questions['Pratiquer des jeux de logique']:
    personality_scores['A']+=1
if questions['Dresser un arbre généalogique']:
    personality_scores['B']+=1
if questions['Prendre la voiture ou le vélo et rouler sans but']:
    personality_scores['D']+=1
if questions['Construire']:
    personality_scores['B']+=1
if questions['Jouer avec des enfants']:
    personality_scores['C']+=1
if questions['Rêver éveillé']:
    personality_scores['D']+=1
if questions['Créer des logos']:
    personality_scores['D']+=1
if questions['Ordre']:
    personality_scores['B']+=1
if questions['Sortir']:
    personality_scores['C']+=1
if questions['Cerf']:
    personality_scores['D']+=1
if questions2['Plat']:
    personality_scores['D']+=1
if questions2['Ordi']:
    personality_scores['A']+=1
if questions2['Réparer']:
    personality_scores['A']+=1
if questions2['Écouter de la musique']:
    personality_scores['C']+=1
if questions2['Coquilles']:
    personality_scores['B']+=1
if questions2['Ressentir une émotion devant un paysage, un tableau ou une scène']:
    personality_scores['C']+=1
if questions2['Bourse']:
    personality_scores['A']+=1
if questions2['Connard']:
    personality_scores['A']+=1
if questions2['Club']:
    personality_scores['C']+=1
if questions2['Pratiquer le modélisme']:
    personality_scores['B']+=1

st.header('Vos phrases et expressions')
st.write('Cochez les expressions que vous utilisez souvent')

col1, col2 = st.columns(2)
with col1:
    phrases = {
        'resultats':st.checkbox("J'attends des résultats concrets."),
        'les i':st.checkbox('Mettre les points sur les i.'),
        'st':st.checkbox('Je suis comme Saint Thomas...'),
        'Tu vois':st.checkbox('Tu vois ce que je veux dire...'),
        'ekip':st.checkbox("Avoir l'esprit d'équipe"),
        'Imaginons que':st.checkbox('Imaginons que...'),
        'Entre bien dans sa peau':st.checkbox('Etre bien dans sa peau.'),
        'danger':st.checkbox("C'est dangereux.")
        }
with col2:
    phrases2 ={
        'Et si...':st.checkbox('Et si...'),
        'Soyons sérieux':st.checkbox('Soyons sérieux.'),
        "Audace":st.checkbox("De l'audace, toujours de..."),
        "J'ai le sentiment que...":st.checkbox("J'ai le sentiments que..."),
        'critique':st.checkbox("Une critique s'impose."),
        'ordre':st.checkbox('Procédons par ordre.'),
        "Nul": st.checkbox("Nul n'est censé ignorer la loi."),
        "valeur":st.checkbox('La valeur humaine')
        }

if phrases['resultats']:
    personality_scores['A']+=1
if phrases['les i']:
    personality_scores['B']+=1
if phrases['st']:
    personality_scores['A']+=1
if phrases['Tu vois']:
    personality_scores['D']+=1
if phrases['ekip']:
    personality_scores['C']+=1
if phrases['Imaginons que']:
    personality_scores['D']+=1
if phrases['Entre bien dans sa peau']:
    personality_scores['C']+=1
if phrases['danger']:
    personality_scores['B']+=1
if phrases2['Et si...']:
    personality_scores['D']+=1
if phrases2['Soyons sérieux']:
    personality_scores['A']+=1
if phrases2["Audace"]:
    personality_scores['D']+=1
if phrases2["J'ai le sentiment que..."]:
    personality_scores['C']+=1
if phrases2['critique']:
    personality_scores['A']+=1
if phrases2['ordre']:
    personality_scores['B']+=1
if phrases2["Nul"]:
    personality_scores['B']+=1
if phrases2["valeur"]:
    personality_scores['C']+=1


submit = st.button('Calculer le résultat')
if submit:
    if max(personality_scores.values()) == 0:
        st.error('Vous devez remplir au moins une des catégories pour pouvoir calculer le résultat', icon='🥺')
    coef = 100/max(personality_scores.values())
    A_score = coef*personality_scores.get('A')
    B_score = coef*personality_scores.get('B')
    C_score = coef*personality_scores.get('C')
    D_score = coef*personality_scores.get('D')
    
    st.write(f'Ingénieur: {A_score}')
    st.write(f'Cartographe: {B_score}')
    st.write(f'Barde: {C_score}')
    st.write(f'Inventeur: {D_score}')
    
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append results to global_results.txt
    append_to_global_results(timestamp, user, orga, A_score, B_score, C_score, D_score)

    # Display the results
    response = post_results_to_database(user, orga, A_score, B_score, C_score, D_score)
    if response.status_code == 201 or response.status_code == 204:
        st.success("Results posted successfully!")
    else:
        st.error(f"Failed to post results: {response.status_code} - {response.text}")

    st.success(f"Results calculated and saved at {timestamp}. A: {A_score}, B: {B_score}, C: {C_score}, D: {D_score}")

    
    scores = {'Ingénieur':A_score, 'Cartographe':B_score, 'Barde': C_score, 'Inventeur':D_score}
    
    pilots = [k for k, v in scores.items() if v>99]
    
    
    # Create a temporary text file with the results
    #result_filename = 'results.txt'
    create_result_text_file(result_filename, user, orga, personality_scores, coef)

    # Send the email
    #result = send_email(subject, body, to_email, smtp_server, smtp_port, smtp_user, smtp_pass)

    #if result:
    #    st.success('Results sent successfully!')
    #else:
    #    st.error('Error sending the results. Please check your email configuration.')
    
    #st.write(f'votre type de personnalité est / vos types de personnalités sont: {pilots}')  
    
    st.header('Vos pilotes')
    
    if 'Ingénieur' in pilots:
        st.image('Inge.png', width=400)
        st.write(A_text)
    if 'Cartographe' in pilots:
        st.image('carto.png', width=400)
        st.write(B_text)
    if 'Barde' in pilots:
        st.image('bard.png', width=400)
        st.write(C_text)
    if 'Inventeur' in pilots:
        st.image('artistii.png', width=400)
        st.write(D_text)
        
    st.header('Vos co-pilotes')
    
    copilots = [k for k, v in scores.items() if v<100 and v>=75]
    
    if len(copilots) == 0:
        st.write("Nous n'avons pas détecté de co-pilote")
    
    if 'Ingénieur' in copilots:
        st.image('Inge.png', width=400)
        st.write(A_text)
    if 'Cartographe' in copilots:
        st.image('carto.png', width=400)
        st.write(B_text)
    if 'Barde' in copilots:
        st.image('bard.png', width=400)
        st.write(C_text)
    if 'Inventeur' in copilots:
        st.image('artistii.png', width=400)
        st.write(D_text)
        
    st.header('Vos failles')
    
    failles = [k for k, v in scores.items() if v<40 and v>15]
    
    if len(failles) == 0:
        st.write("Nous n'avons pas détecté de failles")
    
    if 'Ingénieur' in failles:
        st.image('Inge.png', width=400)
        st.write(A_text)
    if 'Cartographe' in failles:
        st.image('carto.png', width=400)
        st.write(B_text)
    if 'Barde' in failles:
        st.image('bard.png', width=400)
        st.write(C_text)
    if 'Inventeur' in failles:
        st.image('artistii.png', width=400)
        st.write(D_text)
        
    st.header('Vos limites')    
    limites = [k for k, v in scores.items() if v<15]
    
    if len(limites) == 0:
        st.write("Nous n'avons pas détecté de limites")
    
    if 'Ingénieur' in limites:
        st.image('Inge.png', width=400)
        st.write(A_text)
    if 'Cartographe' in limites:
        st.image('carto.png', width=400)
        st.write(B_text)
    if 'Barde' in limites:
        st.image('bard.png', width=400)
        st.write(C_text)
    if 'Inventeur' in limites:
        st.image('artistii.png', width=400)
        st.write(D_text)

        
    # Display the download button
    if os.path.exists(result_filename):
        st.download_button(
            label="Télecharger les Résultats",
            data=open(result_filename, 'rb'),
            key="download_results",
            file_name="results.txt",
            help="Click to download the results as a text file.",
        )