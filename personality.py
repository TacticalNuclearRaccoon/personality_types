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
import plotly.graph_objects as go

#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText

# Define your result_filename and global_results_filename
result_filename = "results.txt"
global_results_filename = "global_results.txt"
icon = "Favicon_2x.ico"

# Inject external CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#post to database
DATABASE_URL = st.secrets["DATABASE_URL"]
DATABASE_API_KEY = st.secrets["DATABASE_API_KEY"]

#the fmunctions below are to prevent the loss of answers if the user accifentally refreshes the page
# Initialize session state from URL parameters on page load

def init_from_url():
    params = st.query_params
    
    # Initialize user and orga from URL
    if 'user' not in st.session_state:
        st.session_state.user = params.get('user', '')
    
    if 'orga' not in st.session_state:
        st.session_state.orga = params.get('orga', '')
    
    # Initialize selections from URL - FIXED to properly filter empty strings
    if 'selected_mots_cles' not in st.session_state:
        mots_param = params.get('mots', '')
        st.session_state.selected_mots_cles = set([m for m in mots_param.split(',') if m]) if mots_param else set()
    
    if 'selected_loisirs' not in st.session_state:
        loisirs_param = params.get('loisirs', '')
        st.session_state.selected_loisirs = set([l for l in loisirs_param.split(',') if l]) if loisirs_param else set()
    
    if 'selected_questions' not in st.session_state:
        questions_param = params.get('questions', '')
        st.session_state.selected_questions = set([q for q in questions_param.split(',') if q]) if questions_param else set()
    
    if 'selected_phrases' not in st.session_state:
        phrases_param = params.get('phrases', '')
        st.session_state.selected_phrases = set([p for p in phrases_param.split(',') if p]) if phrases_param else set()

    if 'selected_activities' not in st.session_state:
        activities_param = params.get('activities', '')
        st.session_state.selected_activities = set([a for a in activities_param.split(',') if a]) if activities_param else set()

# Update URL parameters whenever selections change
def update_url():
    # Filter out empty strings before joining
    mots_str = ','.join([m for m in st.session_state.selected_mots_cles if m]) if st.session_state.selected_mots_cles else ''
    loisirs_str = ','.join([l for l in st.session_state.selected_loisirs if l]) if st.session_state.selected_loisirs else ''
    questions_str = ','.join([q for q in st.session_state.selected_questions if q]) if st.session_state.selected_questions else ''
    phrases_str = ','.join([p for p in st.session_state.selected_phrases if p]) if st.session_state.selected_phrases else ''
    activities_str = ','.join([a for a in st.session_state.selected_activities if a]) if st.session_state.selected_activities else ''
    
    st.query_params.update({
        'user': st.session_state.user,
        'orga': st.session_state.orga,
        'mots': mots_str,
        'loisirs': loisirs_str,
        'questions': questions_str,
        'phrases': phrases_str,
        'activities': activities_str
    })

# Call this at the very start!
init_from_url()

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

# Function to create a horizontal bar chart
def create_bar_chart(score, color):
    fig = go.Figure()
    
    # Background bar (full width, light gray)
    fig.add_trace(go.Bar(
        x=[100],
        y=[''],
        orientation='h',
        marker=dict(
            color='#E8E8F0',  # Light gray background
            line=dict(width=0),
            cornerradius=20  # Rounded corners
        ),
        showlegend=False,
        hoverinfo='none'
    ))
    
    # Foreground bar (actual score)
    fig.add_trace(go.Bar(
        x=[score],
        y=[''],
        orientation='h',
        marker=dict(
            color=color,
            line=dict(width=0),
            cornerradius=20  # Rounded corners
        ),
        showlegend=False,
        hoverinfo='none'
    ))
    
    # Add white dot at the end of the colored bar
    fig.add_trace(go.Scatter(
        x=[score],
        y=[''],
        mode='markers',
        marker=dict(
            size=15,
            color='white',
            line=dict(color=color, width=2)
        ),
        showlegend=False,
        hoverinfo='none'
    ))
    
    fig.update_layout(
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            showticklabels=False
        ),
        barmode='overlay',
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

# Function to display personality card
def display_personality_card(name, score, image_path, description, background_color):
    st.markdown(f"""
        <div style="
            background: {background_color};
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            color: white;
        ">
            <h1 style="color: white; font-size: 48px; margin: 0;">{name}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image_path, width=300)
    
    with col2:
    # Ceate and display bar chart
        color_map = {
            'Ingénieur': "#667eea",
            'Cartographe': "#28961a",
            'Barde': "#f5576c",
            'Inventeur': "#fd9666"
        }
        bar_chart = create_bar_chart(score, color_map.get(name, '#666666'))
        
        # Display bar with score on the right
        subcol1, subcol2 = st.columns([4, 1])
        with subcol1:
            st.plotly_chart(bar_chart, use_container_width=True)
        with subcol2:
            st.markdown(f"<h2 style='margin-top: 10px; color: {color_map.get(name, '#666666')};'>{score:.2f}</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="
            background: {background_color};
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            color: white;
            line-height: 1.8;
        ">
            {description}
        </div>
    """, unsafe_allow_html=True)


st.set_page_config(layout='wide', page_icon=icon, page_title='E-diag Profiler')

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

try:
    st.image('baniere_profiler.png', use_container_width=True)
except:
    st.image('baniere_profiler.png', use_column_width=True)

# User input with session state
user = st.text_input(
    'Renseignez pseudo', 
    value=st.session_state.user,
    placeholder='Votre pseudo ici',
    key='user_input'
)

# Update session state and URL when user types
if user != st.session_state.user:
    st.session_state.user = user
    update_url()

# Function to fetch organizations from database
def get_organizations_from_database():
    url = f"{DATABASE_URL}/rest/v1/organizations"
    headers = {
        "apikey": DATABASE_API_KEY,
        "Authorization": f"Bearer {DATABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            orgs = response.json()
            
            if not orgs:
                st.warning("No organizations found in database")
                return []
            
            names = [org['name'] for org in orgs if org.get("status") == "ongoing"]
            return names
        else:
            st.warning(f"Failed to fetch organizations: {response.status_code}")
            return []
    except Exception as e:
        st.warning(f"Error fetching organizations: {e}")
        return []

# fetch organization list from database
list_of_orga = get_organizations_from_database()
#st.write(list_of_orga)

# Organization selectbox with session state
orga_index = None
if st.session_state.orga and st.session_state.orga in list_of_orga:
    orga_index = list_of_orga.index(st.session_state.orga)

orga = st.selectbox(
    "Choisissez l'id du test",
    list_of_orga,
    index=orga_index,
    placeholder="Choisissez l'id du test",
    key='orga_select'
)

# Update session state and URL when selection changes
if orga != st.session_state.orga:
    st.session_state.orga = orga if orga else ''
    update_url()

personality_scores = {
    'A':0,
    'B':0,
    'C':0,
    'D':0
    }

########## USER INTERFACE ##########

st.header('Activités de Travail')
st.write("Parmi les activités ci-dessous, cochez celles que vous faites bien, ou très bien")

# List of activities
activites = [
    'Analyser',
    'Administrer',
    'Conceptualiser',
    'Exprimer des idées',
    'Synthétiser',
    'Organiser',
    'Rationaliser',
    'Concrétiser',
    'Échanger (contact)',
    'Résoudre des problèmes',
    'Innover',
    'Enseigner/former',
    'Créer',
    'Chiffrer/calculer',
    'Planifier',
    'Animer (réunion)'
]

# Initialize session state for button selections if not exists
if 'selected_activities' not in st.session_state:
    st.session_state.selected_activities = set()

# Create a grid wrapper
cols = st.columns(2)  # or st.columns(3) for 3 columns
for idx, act in enumerate(activites):
    with cols[idx % len(cols)]:
        # Check if this activity is selected
        is_selected = act in st.session_state.selected_activities
        
        # Create button with appropriate styling
        if st.button(
            act, 
            key=f"btn_{act}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            # Toggle selection
            if act in st.session_state.selected_activities:
                st.session_state.selected_activities.remove(act)
            else:
                st.session_state.selected_activities.add(act)
            update_url()  # Save to URL after each change
            st.rerun()

# Calculate personality scores based on selected activities
# Activity to personality type mapping
activity_mapping = {
    'Analyser': 'A',
    'Administrer': 'B',
    'Conceptualiser': 'D',
    'Exprimer des idées': 'C',
    'Synthétiser': 'D',
    'Organiser': 'B',
    'Rationaliser': 'A',
    'Concrétiser': 'B',
    'Échanger (contact)': 'C',
    'Résoudre des problèmes': 'A',
    'Innover': 'D',
    'Enseigner/former': 'C',
    'Créer': 'D',
    'Chiffrer/calculer': 'A',
    'Planifier': 'B',
    'Animer (réunion)': 'C'
}

# Calculate scores
for act in st.session_state.selected_activities:
    if act in activity_mapping:
        personality_scores[activity_mapping[act]] += 1

# Initialize session state for all button selections if not exists
if 'selected_mots_cles' not in st.session_state:
    st.session_state.selected_mots_cles = set()
if 'selected_loisirs' not in st.session_state:
    st.session_state.selected_loisirs = set()
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = set()
if 'selected_phrases' not in st.session_state:
    st.session_state.selected_phrases = set()

# Mapping dictionaries
mots_cles_mapping = {
    'Logique': 'A', 'Serviable': 'C', 'Organisé': 'B', 'Confiant': 'C',
    'Rationnel': 'A', 'Conservateur': 'B', 'Expressif': 'C', 'Analytique': 'A',
    'Émotif': 'C', 'Lecteur technique': 'B', 'Réaliste': 'A', 'Créatif': 'D',
    'Intuitif : sentiments': 'C', 'Passionné': 'C', 'Critique': 'A', 'Amical': 'C',
    'Objectif': 'A', 'Imaginatif': 'D', 'Coopératif': 'C', 'Enthousiaste': 'C',
    'Pondéré': 'A', 'Artistique': 'D', 'Souple': 'C', 'Discret': 'A',
    'Précis': 'A', 'Contrôlé': 'B', 'Sérieux': 'A', 'Tenace': 'B',
    'Minutieux': 'B', 'Intuitif : Solutions': 'D', 'Simultané': 'D',
    'Compétiteur': 'B', 'Aventurier': 'D', 'Ordonné': 'B', 'Libéral': 'D',
    'Discipliné': 'B', 'Curieux': 'D', 'Conventionnel': 'B', 'Original': 'D',
    'Indépendant': 'D'
}

loisirs_mapping = {
    'Photographie': 'D', 'Farniente': 'D', 'Radioamateur': 'A', 'Chasse': 'A',
    'Pêche': 'B', 'Jardinage': 'C', 'Travail du bois': 'A', 'Musique': 'C',
    'Jogging': 'B', 'Réparation de voitures': 'A', 'Chant': 'C', 'Bénévolat': 'C',
    'Lecture': 'C', 'Bricolage': 'A', 'Spectateur sportif': 'B', 'Collections': 'B',
    'Jeux de hasard': 'D', 'Artisanats': 'D', 'Cuisine': 'B', 'Conversations': 'C',
    'Théâtre': 'D', 'Jeux de cartes': 'B', 'Pêche sous marine': 'D', 'Voyages': 'C',
    'Botanique': 'B', 'Golf': 'A', 'Ordinateur': 'A', 'Danse': 'D',
    'Jeux de stratégie': 'D', 'Jeux de logique': 'A', 'Jeux de société': 'C',
    'Bowling': 'B'
}

questions_mapping = {
    'Pratiquer des jeux de logique': 'A',
    'Dresser un arbre généalogique': 'B',
    'Prendre la voiture ou le vélo et rouler sans but': 'D',
    "Construire un article en kit en suivant la notice d'assemblage": 'B',
    'Jouer avec des enfants': 'C',
    'Rêver éveillé': 'D',
    'Créer des logos': 'D',
    "Mettre de l'ordre dans les photographies": 'B',
    'Sortir avec des amis et faire la fête': 'C',
    'Faire voler un cerf-volant': 'D',
    'Préparer un plat de votre invention': 'D',
    'Faire fonctionner (ou apprendre à faire fonctionner) un ordinateur': 'A',
    "Réparer les pannes des machines ou des appareils": 'A',
    'Écouter de la musique': 'C',
    'Repérer des coquilles dans un livre ou des erreurs sur un relevé bancaire': 'B',
    'Ressentir une émotion devant un paysage, un tableau ou une scène': 'C',
    "Adhérer à un club d'investissement en Bourse": 'A',
    "Jouer à l'avocat du diable dans une discussion": 'A',
    'Animer un cercle ou un club': 'C',
    'Pratiquer le modélisme': 'B'
}

phrases_mapping = {
    "J'attends des résultats concrets.": 'A',
    'Mettre les points sur les i.': 'B',
    'Je suis comme Saint Thomas...': 'A',
    'Tu vois ce que je veux dire...': 'D',
    "Avoir l'esprit d'équipe": 'C',
    'Imaginons que...': 'D',
    'Etre bien dans sa peau.': 'C',
    "C'est dangereux.": 'B',
    'Et si...': 'D',
    'Soyons sérieux.': 'A',
    "De l'audace, toujours de...": 'D',
    "J'ai le sentiments que...": 'C',
    "Une critique s'impose.": 'A',
    'Procédons par ordre.': 'B',
    "Nul n'est censé ignorer la loi.": 'B',
    'La valeur humaine': 'C'
}

# --- MOTS CLÉS ---
st.header('Mots clés')
st.write("Dans la liste ci-dessous, sélectionnez 10 adjectifs qui vous caractérisent le mieux")

mots_cles_list = list(mots_cles_mapping.keys())
mid_point = len(mots_cles_list) // 2

col1, col2 = st.columns(2)
with col1:
    for mot in mots_cles_list[:mid_point]:
        is_selected = mot in st.session_state.selected_mots_cles
        if st.button(
            mot,
            key=f"mot_{mot}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if mot in st.session_state.selected_mots_cles:
                st.session_state.selected_mots_cles.remove(mot)
            else:
                st.session_state.selected_mots_cles.add(mot)
            update_url()  # Save to URL after each change
            st.rerun()
            

with col2:
    for mot in mots_cles_list[mid_point:]:
        is_selected = mot in st.session_state.selected_mots_cles
        if st.button(
            mot,
            key=f"mot_{mot}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if mot in st.session_state.selected_mots_cles:
                st.session_state.selected_mots_cles.remove(mot)
            else:
                st.session_state.selected_mots_cles.add(mot)
            update_url()  # Save to URL after each change
            st.rerun()

selected_mots = len(st.session_state.selected_mots_cles)
st.write(f'Vous avez sélectionné {selected_mots} mots clés')

if selected_mots > 10:
    st.error('Vous ne pouvez selectionner que 10 mots clés', icon='😢')

# --- LOISIRS ---
st.header('Loisirs')
st.write('Selectionnez les loisirs que vous pratiquez ou que vous aimeriez pratiquer')

loisirs_list = list(loisirs_mapping.keys())
mid_point_loisirs = len(loisirs_list) // 2

col1, col2 = st.columns(2)
with col1:
    for loisir in loisirs_list[:mid_point_loisirs]:
        is_selected = loisir in st.session_state.selected_loisirs
        if st.button(
            loisir,
            key=f"loisir_{loisir}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if loisir in st.session_state.selected_loisirs:
                st.session_state.selected_loisirs.remove(loisir)
            else:
                st.session_state.selected_loisirs.add(loisir)
            update_url()  # Save to URL after each change
            st.rerun()

with col2:
    for loisir in loisirs_list[mid_point_loisirs:]:
        is_selected = loisir in st.session_state.selected_loisirs
        if st.button(
            loisir,
            key=f"loisir_{loisir}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if loisir in st.session_state.selected_loisirs:
                st.session_state.selected_loisirs.remove(loisir)
            else:
                st.session_state.selected_loisirs.add(loisir)
            update_url()  # Save to URL after each change
            st.rerun()

# --- 20 QUESTIONS ---
st.header('20 Questions')
st.write('Sélectionnez les activités que vous aimez ou aimeriez pratiquer.')

questions_list = list(questions_mapping.keys())
mid_point_questions = len(questions_list) // 2

col1, col2 = st.columns(2)
with col1:
    for question in questions_list[:mid_point_questions]:
        is_selected = question in st.session_state.selected_questions
        if st.button(
            question,
            key=f"question_{question}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if question in st.session_state.selected_questions:
                st.session_state.selected_questions.remove(question)
            else:
                st.session_state.selected_questions.add(question)
            update_url()  # Save to URL after each change
            st.rerun()

with col2:
    for question in questions_list[mid_point_questions:]:
        is_selected = question in st.session_state.selected_questions
        if st.button(
            question,
            key=f"question_{question}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if question in st.session_state.selected_questions:
                st.session_state.selected_questions.remove(question)
            else:
                st.session_state.selected_questions.add(question)
            update_url()  # Save to URL after each change
            st.rerun()

# --- PHRASES ET EXPRESSIONS ---
st.header('Vos phrases et expressions')
st.write('Cochez les expressions que vous utilisez souvent')

phrases_list = list(phrases_mapping.keys())
mid_point_phrases = len(phrases_list) // 2

col1, col2 = st.columns(2)
with col1:
    for phrase in phrases_list[:mid_point_phrases]:
        is_selected = phrase in st.session_state.selected_phrases
        if st.button(
            phrase,
            key=f"phrase_{phrase}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if phrase in st.session_state.selected_phrases:
                st.session_state.selected_phrases.remove(phrase)
            else:
                st.session_state.selected_phrases.add(phrase)
            update_url()  # Save to URL after each change
            st.rerun()

with col2:
    for phrase in phrases_list[mid_point_phrases:]:
        is_selected = phrase in st.session_state.selected_phrases
        if st.button(
            phrase,
            key=f"phrase_{phrase}",
            type="primary" if is_selected else "secondary",
            use_container_width=True
        ):
            if phrase in st.session_state.selected_phrases:
                st.session_state.selected_phrases.remove(phrase)
            else:
                st.session_state.selected_phrases.add(phrase)
            update_url()  # Save to URL after each change
            st.rerun()

# --- CALCULATE PERSONALITY SCORES ---
personality_scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

# Add scores from mots clés
for mot in st.session_state.selected_mots_cles:
    if mot in mots_cles_mapping:
        personality_scores[mots_cles_mapping[mot]] += 1

# Add scores from loisirs
for loisir in st.session_state.selected_loisirs:
    if loisir in loisirs_mapping:
        personality_scores[loisirs_mapping[loisir]] += 1

# Add scores from questions
for question in st.session_state.selected_questions:
    if question in questions_mapping:
        personality_scores[questions_mapping[question]] += 1

# Add scores from phrases
for phrase in st.session_state.selected_phrases:
    if phrase in phrases_mapping:
        personality_scores[phrases_mapping[phrase]] += 1


submit = st.button('Calculer le résultat')
if 'results_posted' not in st.session_state:
    st.session_state['results_posted'] = False

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
    st.session_state['results_posted'] = True
    scores = {
        'Ingénieur': A_score, 
        'Cartographe': B_score, 
        'Barde': C_score, 
        'Inventeur': D_score
    }
    # Create a temporary text file with the results
    create_result_text_file(result_filename, user, orga, personality_scores, coef)
    # Color scheme for each personality
    colors = {
        'Ingénieur': 'linear-gradient(135deg, #b0bbec 0%, #667eea 100%)',
        'Cartographe': 'linear-gradient(135deg, #97d48f 0%, #28961a 100%)',
        'Barde': 'linear-gradient(135deg, #eba8b1 0%, #f5576c 100%)',
        'Inventeur': 'linear-gradient(135deg, #e0bb97 0%, #fd9666 100%)'
    }
    # Solid colors for cards
    solid_colors = {
        'Ingénieur': "#667eea",
        'Cartographe': "#28961a",
        'Barde': "#f5576c",
        'Inventeur': "#fd9666"
    }
    # --- PILOTS (>99) ---
    pilots = [k for k, v in scores.items() if v > 99]
    if pilots:
        st.markdown("<h1 style='text-align: center; margin: 40px 0;'>🚀 Vos pilotes</h1>", unsafe_allow_html=True)
        
        for pilot in pilots:
            if pilot == 'Ingénieur':
                display_personality_card('Ingénieur', A_score, 'Inge.png', A_text, solid_colors['Ingénieur'])
            elif pilot == 'Cartographe':
                display_personality_card('Cartographe', B_score, 'carto.png', B_text, solid_colors['Cartographe'])
            elif pilot == 'Barde':
                display_personality_card('Barde', C_score, 'bard.png', C_text, solid_colors['Barde'])
            elif pilot == 'Inventeur':
                display_personality_card('Inventeur', D_score, 'artistii.png', D_text, solid_colors['Inventeur'])
    # --- CO-PILOTS (75-99) ---
    copilots = [k for k, v in scores.items() if 75 <= v < 100]
    if copilots:
        st.markdown("<h1 style='text-align: center; margin: 40px 0;'>🤝 Vos co-pilotes</h1>", unsafe_allow_html=True)
        
        for copilot in copilots:
            if copilot == 'Ingénieur':
                display_personality_card('Ingénieur', A_score, 'Inge.png', A_text, solid_colors['Ingénieur'])
            elif copilot == 'Cartographe':
                display_personality_card('Cartographe', B_score, 'carto.png', B_text, solid_colors['Cartographe'])
            elif copilot == 'Barde':
                display_personality_card('Barde', C_score, 'bard.png', C_text, solid_colors['Barde'])
            elif copilot == 'Inventeur':
                display_personality_card('Inventeur', D_score, 'artistii.png', D_text, solid_colors['Inventeur'])
    else:
        st.info("Nous n'avons pas détecté de co-pilote")
    # --- FAILLES (15-40) ---
    failles = [k for k, v in scores.items() if 15 < v < 40]
    if failles:
        st.markdown("<h1 style='text-align: center; margin: 40px 0;'>⚠️ Vos failles</h1>", unsafe_allow_html=True)
        
        for faille in failles:
            if faille == 'Ingénieur':
                display_personality_card('Ingénieur', A_score, 'Inge.png', A_text, solid_colors['Ingénieur'])
            elif faille == 'Cartographe':
                display_personality_card('Cartographe', B_score, 'carto.png', B_text, solid_colors['Cartographe'])
            elif faille == 'Barde':
                display_personality_card('Barde', C_score, 'bard.png', C_text, solid_colors['Barde'])
            elif faille == 'Inventeur':
                display_personality_card('Inventeur', D_score, 'artistii.png', D_text, solid_colors['Inventeur'])
    else:
        st.info("Nous n'avons pas détecté de failles")
    # --- LIMITES (<15) ---
    limites = [k for k, v in scores.items() if v <= 15]
    if limites:
        st.markdown("<h1 style='text-align: center; margin: 40px 0;'>🚧 Vos limites</h1>", unsafe_allow_html=True)
        
        for limite in limites:
            if limite == 'Ingénieur':
                display_personality_card('Ingénieur', A_score, 'Inge.png', A_text, solid_colors['Ingénieur'])
            elif limite == 'Cartographe':
                display_personality_card('Cartographe', B_score, 'carto.png', B_text, solid_colors['Cartographe'])
            elif limite == 'Barde':
                display_personality_card('Barde', C_score, 'bard.png', C_text, solid_colors['Barde'])
            elif limite == 'Inventeur':
                display_personality_card('Inventeur', D_score, 'artistii.png', D_text, solid_colors['Inventeur'])
    else:
        st.info("Nous n'avons pas détecté de limites")
    # Display the download button
    if os.path.exists(result_filename):
        st.download_button(
            label="Télecharger les Résultats",
            data=open(result_filename, 'rb'),
            key="download_results",
            file_name="results.txt",
            help="Click to download the results as a text file.",
        )