import streamlit as st
import asyncio
import tempfile
import os
import base64
import re
import subprocess

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Haiti Community Resilience Initiative | GlobalInternet.py",
    layout="wide",
    page_icon="🇭🇹"
)

# ---------- STYLING (LIGHT BLUE THEME) ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #e8f4fd 0%, #cce4f7 100%);
        color: #0b2b3a;
    }
    .main-title {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #4a90d9, #7bb3e8);
        border-radius: 20px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-title h1 { margin: 0; font-size: 2.5rem; }
    .main-title p { margin: 0.5rem 0 0; font-size: 1.2rem; opacity: 0.9; }
    .section-box {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(8px);
        border: 1px solid #88bce0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,80,160,0.08);
    }
    .budget-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #d4e4f0;
    }
    .budget-total {
        font-weight: 700;
        font-size: 1.2rem;
        padding: 12px 0;
        border-top: 2px solid #4a90d9;
        margin-top: 8px;
    }
    .footer {
        text-align: center;
        padding: 20px 0;
        border-top: 1px solid #a0c4e8;
        margin-top: 30px;
        color: #2a4a6a;
        font-size: 0.9rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4a90d9, #7bb3e8) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        box-shadow: 0 2px 8px rgba(74,144,217,0.3) !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 16px rgba(74,144,217,0.4) !important;
    }
    .contact-box {
        background: rgba(255,255,255,0.8);
        border: 1px solid #88bce0;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .contact-box a { color: #4a90d9; text-decoration: none; font-weight: 600; }
    .contact-box a:hover { text-decoration: underline; }
    .dept-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 10px 0;
    }
    .dept-tag {
        background: rgba(74,144,217,0.15);
        border: 1px solid #4a90d9;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.8rem;
        color: #0b2b3a;
    }
</style>
""", unsafe_allow_html=True)

# ---------- UI DICTIONARY (ALL TEXT IN ENGLISH, FRENCH, SPANISH) ----------
UI = {
    "English": {
        "language_label": "🌐 Language",
        "app_title": "🇭🇹 Haiti Community Resilience Initiative",
        "app_subtitle": "Solar-Powered · Water-Secure · Food-Sustainable · Digitally-Connected · All 10 Departments",
        "sidebar_title": "🇭🇹 Haiti Initiative",
        "nav_overview": "1. Overview",
        "nav_challenge": "2. The Challenge",
        "nav_solution": "3. Our Solution",
        "nav_budget": "4. Budget",
        "nav_involved": "5. Get Involved",
        "departments_label": "📍 Departments Targeted",
        "at_a_glance": "🇭🇹 Haiti at a Glance",
        "population": "Population: ~11 million",
        "sunny_days": "Sunny days: 300+/year",
        "status": "Ready for impact across all departments",
        "overview_title": "🎯 Project Overview",
        "overview_text": "**Haiti** is a country of immense potential, blessed with abundant sunshine, fertile land, and a resilient population. Yet millions of Haitians lack reliable electricity, clean water, and internet access. The **Haiti Community Resilience Initiative** is a replicable model designed to be implemented in **all 10 departments** of the country – from Artibonite to Sud-Est.",
        "objectives": "**Key Objectives:**",
        "obj1": "⚡ Provide reliable solar electricity for homes and community spaces",
        "obj2": "💧 Deliver clean drinking water through solar-powered purification",
        "obj3": "🌱 Train families in sustainable gardening on their own land",
        "obj4": "🌐 Connect communities to the global digital economy",
        "obj5": "📚 Create spaces for education, entrepreneurship, and innovation",
        "challenge_title": "⚠️ The Challenge",
        "challenge_table": "| Issue | Current Reality | Impact |\n|-------|-----------------|--------|\n| Electricity | No grid access in rural areas; expensive generators | Limited productivity, no refrigeration, dark evenings |\n| Water | Unsafe sources, latrines still in use | Health risks, waterborne diseases |\n| Internet | Unreliable mobile hotspots | No digital learning, no remote work |\n| Food | Limited access to fresh produce | Poor nutrition, food insecurity |",
        "solution_title": "💡 Our Solution: 3 Phases",
        "phase1_title": "⚡ Phase 1",
        "phase1_sub": "Solar Microgrid",
        "phase1_items": "- 5kW solar array\n- Battery storage\n- Community well pump\n- Water purification system\n- Computer lab power",
        "phase2_title": "🌱 Phase 2",
        "phase2_sub": "Community Gardening",
        "phase2_items": "- Training program\n- Seeds & tools\n- Composting system\n- Rainwater harvesting\n- Market access support",
        "phase3_title": "🌐 Phase 3",
        "phase3_sub": "Digital Hub",
        "phase3_items": "- 10 computers\n- Satellite internet\n- Coding classes\n- Remote work training\n- Global marketplace",
        "budget_title": "💰 Affordable Budget *per community hub*",
        "budget_total": "Total investment: $75,000 USD",
        "budget_items": [
            ("Solar panels & batteries", "$18,000"),
            ("Water well & purification", "$12,000"),
            ("Garden tools & seeds", "$8,000"),
            ("Computers & internet equipment", "$15,000"),
            ("Training & education programs", "$10,000"),
            ("Transport & logistics", "$6,000"),
            ("Project management (12 months)", "$6,000"),
        ],
        "budget_final": "Total: $75,000 USD",
        "involved_title": "🤝 Get Involved",
        "involved_text": "We invite sponsors, investors, and partners to join us in transforming Haiti, one community at a time. Your contribution will:",
        "involved_items": "- 💡 Bring light to families\n- 💧 Provide clean water\n- 🌱 Grow food security\n- 🌐 Connect communities to the world\n- 👩‍🎓 Educate the next generation",
        "involved_note": "**We are open to partnerships at any level.** Whether you can provide funding, equipment, expertise, or networking, your support matters.",
        "contact_title": "📞 Contact Information",
        "contact_name": "**Gesner Deslandes**  \nEngineer-in-Chief at GlobalInternet.py",
        "contact_email": "📧 **Email:** [deslandes78@gmail.com](mailto:deslandes78@gmail.com)",
        "contact_phone": "📱 **Phone:** (509) 4738-5663 (Moncash / Prisme Transfer)",
        "contact_website": "🌐 **Website:** [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)",
        "cta_title": "🇭🇹 Be the Light for Haiti",
        "cta_text": "Your sponsorship can transform communities across all 10 departments. Contact us today to start the conversation.",
        "footer_text": "Built by **Gesner Deslandes**, Engineer‑in‑Chief at GlobalInternet.py  \nSolar-powered • Community-driven • Future-focused • Nation-wide",
        "audio_note": "ℹ️ The AI audio in all languages reads the full page content – including the sidebar and all sections.",
        "btn_en": "🔊 Listen in English",
        "btn_fr": "🔊 Écouter en français",
        "btn_es": "🔊 Escuchar en español",
        "demo_link": "Live Demo: https://grand-go-ve-community-resilience-app-project-1-9sggxdea68njywp.streamlit.app/"
    },
    "French": {
        "language_label": "🌐 Langue",
        "app_title": "🇭🇹 Initiative de Résilience Communautaire d'Haïti",
        "app_subtitle": "Solaire · Sécurité d'eau · Alimentation durable · Connecté numériquement · 10 départements",
        "sidebar_title": "🇭🇹 Initiative Haïti",
        "nav_overview": "1. Aperçu",
        "nav_challenge": "2. Le défi",
        "nav_solution": "3. Notre solution",
        "nav_budget": "4. Budget",
        "nav_involved": "5. Participez",
        "departments_label": "📍 Départements ciblés",
        "at_a_glance": "🇭🇹 Haïti en bref",
        "population": "Population : ~11 millions",
        "sunny_days": "Jours d'ensoleillement : 300+/an",
        "status": "Prêt pour un impact dans tous les départements",
        "overview_title": "🎯 Aperçu du projet",
        "overview_text": "**Haïti** est un pays d'un immense potentiel, béni par un ensoleillement abondant, des terres fertiles et une population résiliente. Pourtant, des millions d'Haïtiens manquent d'électricité fiable, d'eau potable et d'accès à Internet. L'**Initiative de Résilience Communautaire d'Haïti** est un modèle reproductible conçu pour être mis en œuvre dans les **10 départements** du pays – d'Artibonite à Sud-Est.",
        "objectives": "**Objectifs clés :**",
        "obj1": "⚡ Fournir de l'électricité solaire fiable pour les maisons et les espaces communautaires",
        "obj2": "💧 Distribuer de l'eau potable via une purification solaire",
        "obj3": "🌱 Former les familles au jardinage durable sur leurs propres terres",
        "obj4": "🌐 Connecter les communautés à l'économie numérique mondiale",
        "obj5": "📚 Créer des espaces pour l'éducation, l'entrepreneuriat et l'innovation",
        "challenge_title": "⚠️ Le défi",
        "challenge_table": "| Problème | Réalité actuelle | Impact |\n|----------|------------------|--------|\n| Électricité | Pas d'accès au réseau en zone rurale ; générateurs chers | Productivité limitée, pas de réfrigération, soirées sombres |\n| Eau | Sources dangereuses, latrines encore utilisées | Risques sanitaires, maladies hydriques |\n| Internet | Points d'accès mobiles peu fiables | Pas d'apprentissage numérique, pas de travail à distance |\n| Alimentation | Accès limité aux produits frais | Mauvaise nutrition, insécurité alimentaire |",
        "solution_title": "💡 Notre solution en 3 phases",
        "phase1_title": "⚡ Phase 1",
        "phase1_sub": "Micro-réseau solaire",
        "phase1_items": "- Panneau solaire 5kW\n- Batteries de stockage\n- Pompe de puits communautaire\n- Système de purification d'eau\n- Alimentation du laboratoire informatique",
        "phase2_title": "🌱 Phase 2",
        "phase2_sub": "Jardinage communautaire",
        "phase2_items": "- Programme de formation\n- Semences et outils\n- Système de compostage\n- Récupération d'eau de pluie\n- Soutien à l'accès au marché",
        "phase3_title": "🌐 Phase 3",
        "phase3_sub": "Hub numérique",
        "phase3_items": "- 10 ordinateurs\n- Internet par satellite\n- Cours de codage\n- Formation au travail à distance\n- Accès au marché mondial",
        "budget_title": "💰 Budget abordable *par hub communautaire*",
        "budget_total": "Investissement total : 75 000 USD",
        "budget_items": [
            ("Panneaux solaires et batteries", "18 000 $"),
            ("Puits et purification d'eau", "12 000 $"),
            ("Outils et semences de jardin", "8 000 $"),
            ("Ordinateurs et équipements Internet", "15 000 $"),
            ("Formation et programmes éducatifs", "10 000 $"),
            ("Transport et logistique", "6 000 $"),
            ("Gestion de projet (12 mois)", "6 000 $"),
        ],
        "budget_final": "Total : 75 000 USD",
        "involved_title": "🤝 Participez",
        "involved_text": "Nous invitons les sponsors, investisseurs et partenaires à se joindre à nous pour transformer Haïti, une communauté à la fois. Votre contribution :",
        "involved_items": "- 💡 Apportera la lumière aux familles\n- 💧 Fournira de l'eau potable\n- 🌱 Améliorera la sécurité alimentaire\n- 🌐 Connectera les communautés au monde\n- 👩‍🎓 Éduquera la prochaine génération",
        "involved_note": "**Nous sommes ouverts aux partenariats à tous les niveaux.** Que vous puissiez fournir du financement, de l'équipement, de l'expertise ou du réseautage, votre soutien est important.",
        "contact_title": "📞 Coordonnées",
        "contact_name": "**Gesner Deslandes**  \nIngénieur en chef chez GlobalInternet.py",
        "contact_email": "📧 **Email :** [deslandes78@gmail.com](mailto:deslandes78@gmail.com)",
        "contact_phone": "📱 **Téléphone :** (509) 4738-5663 (Moncash / Prisme Transfer)",
        "contact_website": "🌐 **Site web :** [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)",
        "cta_title": "🇭🇹 Soyez la lumière pour Haïti",
        "cta_text": "Votre parrainage peut transformer des communautés dans les 10 départements. Contactez-nous dès aujourd'hui pour lancer la conversation.",
        "footer_text": "Construit par **Gesner Deslandes**, ingénieur en chef chez GlobalInternet.py  \nSolaire · Communautaire · Tourné vers l'avenir · National",
        "audio_note": "ℹ️ L'audio IA dans les trois langues lit tout le contenu de la page – y compris la barre latérale et toutes les sections.",
        "btn_en": "🔊 Listen in English",
        "btn_fr": "🔊 Écouter en français",
        "btn_es": "🔊 Escuchar en español",
        "demo_link": "Demo en directo: https://grand-go-ve-community-resilience-app-project-1-9sggxdea68njywp.streamlit.app/"
    },
    "Spanish": {
        "language_label": "🌐 Idioma",
        "app_title": "🇭🇹 Iniciativa de Resiliencia Comunitaria de Haití",
        "app_subtitle": "Energía Solar · Agua Segura · Alimentación Sostenible · Conectividad Digital · Los 10 Departamentos",
        "sidebar_title": "🇭🇹 Iniciativa Haití",
        "nav_overview": "1. Resumen",
        "nav_challenge": "2. El desafío",
        "nav_solution": "3. Nuestra solución",
        "nav_budget": "4. Presupuesto",
        "nav_involved": "5. Participe",
        "departments_label": "📍 Departamentos objetivo",
        "at_a_glance": "🇭🇹 Haití de un vistazo",
        "population": "Población: ~11 millones",
        "sunny_days": "Días soleados: 300+/año",
        "status": "Listo para impacto en todos los departamentos",
        "overview_title": "🎯 Resumen del proyecto",
        "overview_text": "**Haití** es un país de inmenso potencial, bendecido con abundante sol, tierras fértiles y una población resiliente. Sin embargo, millones de haitianos carecen de electricidad confiable, agua potable y acceso a Internet. La **Iniciativa de Resiliencia Comunitaria de Haití** es un modelo replicable diseñado para implementarse en los **10 departamentos** del país – desde Artibonite hasta Sud-Est.",
        "objectives": "**Objetivos clave:**",
        "obj1": "⚡ Proporcionar electricidad solar confiable para hogares y espacios comunitarios",
        "obj2": "💧 Entregar agua potable mediante purificación solar",
        "obj3": "🌱 Capacitar a familias en jardinería sostenible en sus propias tierras",
        "obj4": "🌐 Conectar comunidades a la economía digital global",
        "obj5": "📚 Crear espacios para educación, emprendimiento e innovación",
        "challenge_title": "⚠️ El desafío",
        "challenge_table": "| Problema | Realidad actual | Impacto |\n|----------|-----------------|--------|\n| Electricidad | Sin acceso a la red en zonas rurales; generadores caros | Productividad limitada, sin refrigeración, noches oscuras |\n| Agua | Fuentes inseguras, letrinas aún en uso | Riesgos sanitarios, enfermedades hídricas |\n| Internet | Puntos de acceso móvil poco fiables | Sin aprendizaje digital, sin trabajo remoto |\n| Alimentación | Acceso limitado a productos frescos | Mala nutrición, inseguridad alimentaria |",
        "solution_title": "💡 Nuestra solución en 3 fases",
        "phase1_title": "⚡ Fase 1",
        "phase1_sub": "Microrred solar",
        "phase1_items": "- Panel solar 5kW\n- Baterías de almacenamiento\n- Bomba de pozo comunitario\n- Sistema de purificación de agua\n- Alimentación del laboratorio informático",
        "phase2_title": "🌱 Fase 2",
        "phase2_sub": "Jardinería comunitaria",
        "phase2_items": "- Programa de formación\n- Semillas y herramientas\n- Sistema de compostaje\n- Captación de agua de lluvia\n- Apoyo para acceso al mercado",
        "phase3_title": "🌐 Fase 3",
        "phase3_sub": "Centro digital",
        "phase3_items": "- 10 computadoras\n- Internet satelital\n- Clases de programación\n- Capacitación en trabajo remoto\n- Acceso al mercado global",
        "budget_title": "💰 Presupuesto asequible *por centro comunitario*",
        "budget_total": "Inversión total: $75,000 USD",
        "budget_items": [
            ("Paneles solares y baterías", "$18,000"),
            ("Pozo y purificación de agua", "$12,000"),
            ("Herramientas y semillas de jardín", "$8,000"),
            ("Computadoras y equipos de Internet", "$15,000"),
            ("Programas de formación y educación", "$10,000"),
            ("Transporte y logística", "$6,000"),
            ("Gestión del proyecto (12 meses)", "$6,000"),
        ],
        "budget_final": "Total: $75,000 USD",
        "involved_title": "🤝 Participe",
        "involved_text": "Invitamos a patrocinadores, inversores y socios a unirse a nosotros para transformar Haití, una comunidad a la vez. Su contribución:",
        "involved_items": "- 💡 Traerá luz a las familias\n- 💧 Proporcionará agua potable\n- 🌱 Mejorará la seguridad alimentaria\n- 🌐 Conectará comunidades al mundo\n- 👩‍🎓 Educará a la próxima generación",
        "involved_note": "**Estamos abiertos a alianzas a todos los niveles.** Ya sea que pueda proporcionar financiamiento, equipos, experiencia o contactos, su apoyo es importante.",
        "contact_title": "📞 Información de contacto",
        "contact_name": "**Gesner Deslandes**  \nIngeniero Jefe en GlobalInternet.py",
        "contact_email": "📧 **Correo:** [deslandes78@gmail.com](mailto:deslandes78@gmail.com)",
        "contact_phone": "📱 **Teléfono:** (509) 4738-5663 (Moncash / Prisme Transfer)",
        "contact_website": "🌐 **Sitio web:** [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)",
        "cta_title": "🇭🇹 Sea la luz para Haití",
        "cta_text": "Su patrocinio puede transformar comunidades en los 10 departamentos. Contáctenos hoy para iniciar la conversación.",
        "footer_text": "Construido por **Gesner Deslandes**, Ingeniero Jefe en GlobalInternet.py  \nEnergía solar · Impulsado por la comunidad · Enfocado al futuro · Nacional",
        "audio_note": "ℹ️ El audio IA en los tres idiomas lee todo el contenido de la página – incluyendo la barra lateral y todas las secciones.",
        "btn_en": "🔊 Listen in English",
        "btn_fr": "🔊 Écouter en français",
        "btn_es": "🔊 Escuchar en español",
        "demo_link": "Demo en vivo: https://grand-go-ve-community-resilience-app-project-1-9sggxdea68njywp.streamlit.app/"
    }
}

# ---------- SESSION STATE ----------
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# ---------- SIDEBAR ----------
lang = st.session_state.lang
ui = UI[lang]

with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=60)
    st.markdown(f"## {ui['sidebar_title']}")
    st.markdown("---")
    st.markdown("### Project Navigator")
    st.markdown(ui['nav_overview'])
    st.markdown(ui['nav_challenge'])
    st.markdown(ui['nav_solution'])
    st.markdown(ui['nav_budget'])
    st.markdown(ui['nav_involved'])
    st.markdown("---")
    st.markdown(f"### {ui['departments_label']}")
    st.markdown('<div class="dept-list">', unsafe_allow_html=True)
    departments = [
        "Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord",
        "Nord-Est", "Nord-Ouest", "Ouest", "Sud", "Sud-Est"
    ]
    for dept in departments:
        st.markdown(f'<span class="dept-tag">{dept}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"### {ui['at_a_glance']}")
    st.markdown(ui['population'])
    st.markdown(ui['sunny_days'])
    st.markdown(ui['status'])
    st.markdown("---")
    lang_choice = st.selectbox(
        ui['language_label'],
        options=["English", "French", "Spanish"],
        index=["English", "French", "Spanish"].index(st.session_state.lang),
        key="lang_select"
    )
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

# ---------- NARRATION SCRIPTS (Full Content in Each Language) ----------
ENGLISH_SCRIPT = """
Haiti Community Resilience Initiative. Solar-Powered, Water-Secure, Food-Sustainable, Digitally-Connected – for all 10 departments of Haiti.

Project Overview. Haiti is a country of immense potential, blessed with abundant sunshine, fertile land, and a resilient population. Yet millions of Haitians lack reliable electricity, clean water, and internet access. The Haiti Community Resilience Initiative is a replicable model designed to be implemented in every department of the country – from Artibonite to Sud-Est.

The key objectives are: provide reliable solar electricity for homes and community spaces. Deliver clean drinking water through solar-powered purification. Train families in sustainable gardening on their own land. Connect communities to the global digital economy. Create spaces for education, entrepreneurship, and innovation.

The Challenge. Across all departments, the majority of rural areas have no access to the electrical grid, and generators are prohibitively expensive. Unsafe water sources and latrines cause widespread health problems. Internet access is unreliable, preventing digital learning and remote work. Food insecurity is chronic due to limited access to fresh produce.

Our Solution in Three Phases. Phase One: Solar Microgrid. This includes a five-kilowatt solar array, battery storage, a community well pump, water purification system, and power for a computer lab. Phase Two: Community Gardening. This provides training programs, seeds, tools, composting systems, rainwater harvesting, and market access support. Phase Three: Digital Hub. This includes ten computers, satellite internet, coding classes, remote work training, and access to the global marketplace.

The affordable budget totals seventy-five thousand US dollars per hub. Breakdown: solar panels and batteries, eighteen thousand. Water well and purification, twelve thousand. Garden tools and seeds, eight thousand. Computers and internet equipment, fifteen thousand. Training and education programs, ten thousand. Transport and logistics, six thousand. Project management for twelve months, six thousand. Total investment: seventy-five thousand US dollars per community hub.

Get Involved. We invite sponsors, investors, and partners to join us in transforming Haiti, one community at a time. Your contribution will bring light to families, provide clean water, grow food security, connect communities to the world, and educate the next generation. We are open to partnerships at any level. Whether you can provide funding, equipment, expertise, or networking, your support matters.

Contact Information. Gesner Deslandes, Engineer-in-Chief at GlobalInternet.py. Email: deslandes78@gmail.com. Phone: (509) 4738-5663. Website: globalinternetsitepy.streamlit.app.

Be the Light for Haiti. Your sponsorship can transform communities across all 10 departments. Contact us today to start the conversation.

Built by Gesner Deslandes, Engineer-in-Chief at GlobalInternet.py. Solar-powered, Community-driven, Future-focused.

Now, let's look at the sidebar. The sidebar lists the project navigator with sections: Overview, The Challenge, Our Solution, Budget, and Get Involved. It also shows all ten departments where this initiative can be implemented: Artibonite, Centre, Grand'Anse, Nippes, Nord, Nord-Est, Nord-Ouest, Ouest, Sud, and Sud-Est. Haiti has a population of about 11 million, over 300 sunny days per year, and is ready for impact across all departments.

Conclusion. How is this project possible? It is possible because we combine proven technologies with local knowledge and community participation. The abundant sunshine provides free energy. The fertile land can grow food. The people have the will and the skills to make it work. With the right partnership and modest investment, we can turn this vision into reality. We invite all sponsors to visit the live demo of this project at the following link: https://grand-go-ve-community-resilience-app-project-1-9sggxdea68njywp.streamlit.app/ to see the full proposal and interactive budget breakdown. Together, we can build resilience, dignity, and hope for all of Haiti. Thank you for your support.
"""

FRENCH_SCRIPT = """
Initiative de Résilience Communautaire d'Haïti. Solaire, Sécurité d'eau, Alimentation durable, Connecté numériquement – pour les 10 départements d'Haïti.

Aperçu du projet. Haïti est un pays d'un immense potentiel, béni par un ensoleillement abondant, des terres fertiles et une population résiliente. Pourtant, des millions d'Haïtiens manquent d'électricité fiable, d'eau potable et d'accès à Internet. L'Initiative de Résilience Communautaire d'Haïti est un modèle reproductible conçu pour être mis en œuvre dans chaque département du pays – d'Artibonite à Sud-Est.

Les objectifs clés sont : fournir de l'électricité solaire fiable pour les maisons et les espaces communautaires. Distribuer de l'eau potable via une purification solaire. Former les familles au jardinage durable sur leurs propres terres. Connecter les communautés à l'économie numérique mondiale. Créer des espaces pour l'éducation, l'entrepreneuriat et l'innovation.

Le défi. Dans tous les départements, la majorité des zones rurales n'ont pas accès au réseau électrique, et les générateurs sont prohibitifs. Les sources d'eau sont dangereuses, avec des latrines encore utilisées, causant des problèmes de santé généralisés. L'accès à Internet est peu fiable, empêchant l'apprentissage numérique et le travail à distance. L'insécurité alimentaire est chronique en raison d'un accès limité aux produits frais.

Notre solution en trois phases. Phase un : micro-réseau solaire. Cela comprend un panneau solaire de cinq kilowatts, des batteries, une pompe de puits communautaire, un système de purification d'eau et l'alimentation d'un laboratoire informatique. Phase deux : jardinage communautaire. Cela offre des programmes de formation, des semences, des outils, des systèmes de compostage, la récupération d'eau de pluie et un soutien à l'accès au marché. Phase trois : hub numérique. Cela comprend dix ordinateurs, un accès Internet par satellite, des cours de codage, une formation au travail à distance et un accès au marché mondial.

Le budget abordable totalise soixante-quinze mille dollars américains par hub. Détails : panneaux solaires et batteries, dix-huit mille. Puits et purification d'eau, douze mille. Outils et semences de jardin, huit mille. Ordinateurs et équipements Internet, quinze mille. Formation et programmes éducatifs, dix mille. Transport et logistique, six mille. Gestion de projet pendant douze mois, six mille. Investissement total : soixante-quinze mille dollars américains par hub communautaire.

Participez. Nous invitons les sponsors, investisseurs et partenaires à se joindre à nous pour transformer Haïti, une communauté à la fois. Votre contribution apportera la lumière aux familles, fournira de l'eau potable, améliorera la sécurité alimentaire, connectera les communautés au monde et éduquera la prochaine génération. Nous sommes ouverts aux partenariats à tous les niveaux. Que vous puissiez fournir du financement, de l'équipement, de l'expertise ou du réseautage, votre soutien est important.

Coordonnées. Gesner Deslandes, ingénieur en chef chez GlobalInternet.py. Email : deslandes78@gmail.com. Téléphone : (509) 4738-5663. Site web : globalinternetsitepy.streamlit.app.

Soyez la lumière pour Haïti. Votre parrainage peut transformer des communautés dans les 10 départements. Contactez-nous dès aujourd'hui pour lancer la conversation.

Construit par Gesner Deslandes, ingénieur en chef chez GlobalInternet.py. Solaire, communautaire, tourné vers l'avenir.

Parlons maintenant de la barre latérale. La barre latérale contient le navigateur de projet avec les sections : Aperçu, Le défi, Notre solution, Budget et Participez. Elle liste les dix départements ciblés : Artibonite, Centre, Grand'Anse, Nippes, Nord, Nord-Est, Nord-Ouest, Ouest, Sud et Sud-Est. Elle indique également qu'Haïti a une population d'environ 11 millions d'habitants, plus de 300 jours d'ensoleillement par an, et est prête pour un impact dans tous les départements.

Conclusion. Comment ce projet est-il possible ? Il est possible parce que nous combinons des technologies éprouvées avec les connaissances locales et la participation communautaire. Le soleil abondant fournit de l'énergie gratuite. La terre fertile peut produire de la nourriture. Les gens ont la volonté et les compétences pour le faire fonctionner. Avec le bon partenariat et un investissement modeste, nous pouvons transformer cette vision en réalité. Nous invitons tous les sponsors à visiter la démo en direct de ce projet à l'adresse suivante : https://grand-go-ve-community-resilience-app-project-1-9sggxdea68njywp.streamlit.app/ pour voir la proposition complète et le budget interactif. Ensemble, nous pouvons bâtir la résilience, la dignité et l'espoir pour toute la nation haïtienne. Merci pour votre soutien.
"""

SPANISH_SCRIPT = """
Iniciativa de Resiliencia Comunitaria de Haití. Energía Solar, Agua Segura, Alimentación Sostenible, Conectividad Digital – para los 10 departamentos de Haití.

Resumen del proyecto. Haití es un país de inmenso potencial, bendecido con abundante sol, tierras fértiles y una población resiliente. Sin embargo, millones de haitianos carecen de electricidad confiable, agua potable y acceso a Internet. La Iniciativa de Resiliencia Comunitaria de Haití es un modelo replicable diseñado para implementarse en cada departamento del país – desde Artibonite hasta Sud-Est.

Los objetivos clave son: proporcionar electricidad solar confiable para hogares y espacios comunitarios. Entregar agua potable mediante purificación solar. Capacitar a familias en jardinería sostenible en sus propias tierras. Conectar comunidades a la economía digital global. Crear espacios para educación, emprendimiento e innovación.

El desafío. En todos los departamentos, la mayoría de las zonas rurales no tienen acceso a la red eléctrica, y los generadores son prohibitivos. Las fuentes de agua son inseguras, con letrinas aún en uso, causando problemas de salud generalizados. El acceso a Internet es poco fiable, impidiendo el aprendizaje digital y el trabajo remoto. La inseguridad alimentaria es crónica debido al acceso limitado a productos frescos.

Nuestra solución en tres fases. Fase uno: microrred solar. Esto incluye un panel solar de cinco kilovatios, baterías, una bomba de pozo comunitario, un sistema de purificación de agua y alimentación para un laboratorio informático. Fase dos: jardinería comunitaria. Esto ofrece programas de formación, semillas, herramientas, sistemas de compostaje, captación de agua de lluvia y apoyo para acceso al mercado. Fase tres: centro digital. Esto incluye diez computadoras, Internet satelital, clases de programación, capacitación en trabajo remoto y acceso al mercado global.

El presupuesto asequible totaliza setenta y cinco mil dólares estadounidenses por centro. Detalles: paneles solares y baterías, dieciocho mil. Pozo y purificación de agua, doce mil. Herramientas y semillas de jardín, ocho mil. Computadoras y equipos de Internet, quince mil. Programas de formación y educación, diez mil. Transporte y logística, seis mil. Gestión del proyecto durante doce meses, seis mil. Inversión total: setenta y cinco mil dólares estadounidenses por centro comunitario.

Participe. Invitamos a patrocinadores, inversores y socios a unirse a nosotros para transformar Haití, una comunidad a la vez. Su contribución traerá luz a las familias, proporcionará agua potable, mejorará la seguridad alimentaria, conectará comunidades al mundo y educará a la próxima generación. Estamos abiertos a alianzas a todos los niveles. Ya sea que pueda proporcionar financiamiento, equipos, experiencia o contactos, su apoyo es importante.

Información de contacto. Gesner Deslandes, Ingeniero Jefe en GlobalInternet.py. Correo: deslandes78@gmail.com. Teléfono: (509) 4738-5663. Sitio web: globalinternetsitepy.streamlit.app.

Sea la luz para Haití. Su patrocinio puede transformar comunidades en los 10 departamentos. Contáctenos hoy para iniciar la conversación.

Construido por Gesner Deslandes, Ingeniero Jefe en GlobalInternet.py. Energía solar, impulsado por la comunidad, enfocado al futuro.

Ahora, veamos la barra lateral. La barra lateral contiene el navegador del proyecto con las secciones: Resumen, El desafío, Nuestra solución, Presupuesto y Participe. También enumera los diez departamentos objetivo: Artibonite, Centre, Grand'Anse, Nippes, Nord, Nord-Est, Nord-Ouest, Ouest, Sud y Sud-Est. Haití tiene una población de aproximadamente 11 millones, más de 300 días soleados al año, y está listo para tener impacto en todos los departamentos.

Conclusión. ¿Cómo es posible este proyecto? Es posible porque combinamos tecnologías probadas con conocimientos locales y participación comunitaria. El sol abundante proporciona energía gratuita. La tierra fértil puede producir alimentos. La gente tiene la voluntad y las habilidades para hacerlo funcionar. Con la alianza adecuada y una inversión modesta, podemos convertir esta visión en realidad. Invitamos a todos los patrocinadores a visitar la demo en vivo de este proyecto en el siguiente enlace: https://grand-go-ve-community-resilience-app-project-1-9sggxdea68njywp.streamlit.app/ para ver la propuesta completa y el presupuesto interactivo. Juntos, podemos construir resiliencia, dignidad y esperanza para toda Haití. Gracias por su apoyo.
"""

# ---------- AUDIO FUNCTIONS ----------
def split_text_into_chunks(text, max_chars=1500):
    sentences = re.split(r'(?<=[。！？.!?])', text)
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) <= max_chars:
            current += sent
        else:
            if current:
                chunks.append(current.strip())
            current = sent
    if current:
        chunks.append(current.strip())
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chars:
            final_chunks.append(chunk)
        else:
            words = chunk.split()
            part = ""
            for word in words:
                if len(part) + len(word) + 1 <= max_chars:
                    part += " " + word
                else:
                    if part:
                        final_chunks.append(part.strip())
                    part = word
            if part:
                final_chunks.append(part.strip())
    return final_chunks

async def generate_audio(text, voice):
    try:
        import edge_tts
        # Try full text first
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                output_path = tmp.name
            comm = edge_tts.Communicate(text, voice)
            await comm.save(output_path)
            if os.path.getsize(output_path) > 0:
                return output_path
        except Exception as e:
            st.warning(f"Full text generation failed: {e}. Trying chunked fallback...")

        chunks = split_text_into_chunks(text, 1000)
        temp_files = []
        for i, chunk in enumerate(chunks):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    temp_path = tmp.name
                comm = edge_tts.Communicate(chunk, voice)
                await comm.save(temp_path)
                if os.path.getsize(temp_path) > 0:
                    temp_files.append(temp_path)
            except Exception as e:
                st.error(f"Chunk {i+1} failed: {e}")
        if not temp_files:
            return None

        # Check ffmpeg availability
        ffmpeg_available = False
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            ffmpeg_available = True
        except:
            ffmpeg_available = False

        if ffmpeg_available and len(temp_files) > 1:
            concat_file = "concat_list.txt"
            with open(concat_file, "w") as f:
                for tf in temp_files:
                    f.write(f"file '{tf}'\n")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                output_path = tmp.name
            cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", output_path, "-y"]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                for tf in temp_files:
                    os.remove(tf)
                os.remove(concat_file)
                return output_path
            except Exception as e:
                st.error(f"FFmpeg concatenation failed: {e}. Playing first chunk only.")
                return temp_files[0] if temp_files else None
        else:
            return temp_files[0] if temp_files else None
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None

def play_audio(audio_files):
    if isinstance(audio_files, list):
        if not audio_files:
            return
        html = """
        <div id="audio-container"></div>
        <script>
        (function() {
            const container = document.getElementById('audio-container');
            const audioSources = [];
        """
        for path in audio_files:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    html += f"audioSources.push('data:audio/mp3;base64,{b64}');\n"
        html += """
            let index = 0;
            function playNext() {
                if (index >= audioSources.length) return;
                const audio = document.createElement('audio');
                audio.src = audioSources[index];
                audio.controls = true;
                audio.autoplay = true;
                audio.style.width = '100%';
                container.appendChild(audio);
                audio.onended = function() {
                    index++;
                    playNext();
                };
            }
            playNext();
        })();
        </script>
        """
        st.markdown(html, unsafe_allow_html=True)
    else:
        if audio_files and os.path.exists(audio_files):
            with open(audio_files, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width:100%;"></audio>', unsafe_allow_html=True)
            os.unlink(audio_files)

# ---------- MAIN CONTENT ----------
st.markdown(f"""
<div class="main-title">
    <h1>{ui['app_title']}</h1>
    <p>{ui['app_subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# Audio buttons (three now)
col_audio1, col_audio2, col_audio3 = st.columns(3)
with col_audio1:
    if st.button(ui['btn_en'], key="en_btn", use_container_width=False):
        with st.spinner("Generating English audio..."):
            audio_files = asyncio.run(generate_audio(ENGLISH_SCRIPT, "en-US-JennyNeural"))
            if audio_files:
                play_audio(audio_files)
            else:
                st.error("Failed to generate audio.")

with col_audio2:
    if st.button(ui['btn_fr'], key="fr_btn", use_container_width=False):
        with st.spinner("Génération de l'audio français..."):
            audio_files = asyncio.run(generate_audio(FRENCH_SCRIPT, "fr-FR-DeniseNeural"))
            if audio_files:
                play_audio(audio_files)
            else:
                st.error("Échec de la génération audio.")

with col_audio3:
    if st.button(ui['btn_es'], key="es_btn", use_container_width=False):
        with st.spinner("Generando audio en español..."):
            audio_files = asyncio.run(generate_audio(SPANISH_SCRIPT, "es-ES-ElviraNeural"))
            if audio_files:
                play_audio(audio_files)
            else:
                st.error("Fallo al generar audio.")

# ---------- PROJECT OVERVIEW ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown(f"### {ui['overview_title']}")
st.markdown(ui['overview_text'])
st.markdown(f"{ui['objectives']}")
st.markdown(f"- {ui['obj1']}")
st.markdown(f"- {ui['obj2']}")
st.markdown(f"- {ui['obj3']}")
st.markdown(f"- {ui['obj4']}")
st.markdown(f"- {ui['obj5']}")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- THE CHALLENGE ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown(f"### {ui['challenge_title']}")
st.markdown(ui['challenge_table'])
st.markdown('</div>', unsafe_allow_html=True)

# ---------- SOLUTION ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown(f"### {ui['solution_title']}")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"#### {ui['phase1_title']}")
    st.markdown(f"**{ui['phase1_sub']}**")
    st.markdown(ui['phase1_items'])
with col2:
    st.markdown(f"#### {ui['phase2_title']}")
    st.markdown(f"**{ui['phase2_sub']}**")
    st.markdown(ui['phase2_items'])
with col3:
    st.markdown(f"#### {ui['phase3_title']}")
    st.markdown(f"**{ui['phase3_sub']}**")
    st.markdown(ui['phase3_items'])
st.markdown('</div>', unsafe_allow_html=True)

# ---------- BUDGET ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown(f"### {ui['budget_title']}")
st.markdown(f"*{ui['budget_total']}*")
st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
for item, cost in ui['budget_items']:
    st.markdown(f'<div class="budget-row"><span>{item}</span><span>{cost}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="budget-total">{ui["budget_final"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CONTACT & SUPPORT ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown(f"### {ui['involved_title']}")
st.markdown(ui['involved_text'])
st.markdown(ui['involved_items'])
st.markdown(ui['involved_note'])

st.markdown('<div class="contact-box">', unsafe_allow_html=True)
st.markdown(f"### {ui['contact_title']}")
st.markdown(ui['contact_name'])
st.markdown(ui['contact_email'])
st.markdown(ui['contact_phone'])
st.markdown(ui['contact_website'])
st.markdown(f"**{ui['demo_link']}**")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CALL TO ACTION ----------
st.markdown(f"""
<div style="background: linear-gradient(135deg, #4a90d9, #7bb3e8); border-radius: 16px; padding: 2rem; text-align: center; color: white; margin-top: 1rem;">
    <h2 style="margin: 0; color: white;">{ui['cta_title']}</h2>
    <p style="font-size: 1.1rem; opacity: 0.95;">{ui['cta_text']}</p>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(f"""
<div class="footer">
    {ui['footer_text']}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<small style="color: #4a6a8a;">{ui['audio_note']}</small>
""", unsafe_allow_html=True)
