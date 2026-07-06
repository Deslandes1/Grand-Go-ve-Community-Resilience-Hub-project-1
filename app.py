import streamlit as st
import asyncio
import tempfile
import os
import base64
import edge_tts

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Grand Goâve Community Hub | GlobalInternet.py",
    layout="wide",
    page_icon="🌞"
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
    .audio-btn {
        background: #4a90d9 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 0.3rem 1.2rem !important;
        font-size: 0.9rem !important;
        border: none !important;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(74,144,217,0.2) !important;
    }
    .audio-btn:hover {
        background: #7bb3e8 !important;
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# ---------- AUDIO SCRIPTS ----------
ENGLISH_SCRIPT = """
Grand Goâve Community Resilience Hub – A Project by GlobalInternet.py.

Imagine a community where solar power brings light and clean water, where families grow their own food, and where children have access to digital learning. This is not a dream. This is the Grand Goâve Community Resilience Hub.

Located in the peaceful southern region of Haiti, Grand Goâve has abundant sunshine, fertile land, and hardworking people. But they lack reliable electricity, clean water, and internet access.

Our project solves these challenges. Phase one installs a solar microgrid that powers a community well, a water purification system, and a small computer lab. Phase two establishes a community garden training program, teaching families to grow nutritious food on their own land. Phase three creates a digital hub where students can learn, entrepreneurs can connect, and the community can access global opportunities.

The total investment needed is seventy-five thousand US dollars. This covers solar panels, water systems, garden tools, internet equipment, and training costs. With this support, we will transform lives and create a model that can be replicated across Haiti.

We invite sponsors and investors to partner with us. Your contribution will directly impact families, children, and the future of Grand Goâve. Together, we can build resilience, dignity, and hope.

For more information, contact Gesner Deslandes by email at deslandes78@gmail.com or by phone at (509) 4738-5663. Thank you for your support.
"""

FRENCH_SCRIPT = """
Projet Hub de Résilience Communautaire de Grand Goâve – Un projet de GlobalInternet.py.

Imaginez une communauté où l'énergie solaire apporte lumière et eau potable, où les familles cultivent leur propre nourriture, et où les enfants ont accès à l'apprentissage numérique. Ce n'est pas un rêve. C'est le Hub de Résilience Communautaire de Grand Goâve.

Située dans la paisible région sud d'Haïti, Grand Goâve bénéficie d'un ensoleillement abondant, de terres fertiles et de travailleurs acharnés. Mais ils manquent d'électricité fiable, d'eau potable et d'accès à Internet.

Notre projet relève ces défis. La première phase installe un micro-réseau solaire qui alimente un puits communautaire, un système de purification d'eau et un petit laboratoire informatique. La deuxième phase établit un programme de formation au jardinage communautaire, enseignant aux familles comment cultiver des aliments nutritifs sur leurs propres terres. La troisième phase crée un hub numérique où les étudiants peuvent apprendre, les entrepreneurs peuvent se connecter et la communauté peut accéder aux opportunités mondiales.

L'investissement total nécessaire est de soixante-quinze mille dollars américains. Cela couvre les panneaux solaires, les systèmes d'eau, les outils de jardinage, les équipements Internet et les coûts de formation. Avec ce soutien, nous transformerons des vies et créerons un modèle qui pourra être reproduit dans toute la région.

Nous invitons les sponsors et les investisseurs à s'associer à nous. Votre contribution aura un impact direct sur les familles, les enfants et l'avenir de Grand Goâve. Ensemble, nous pouvons bâtir la résilience, la dignité et l'espoir.

Pour plus d'informations, contactez Gesner Deslandes par email à deslandes78@gmail.com ou par téléphone au (509) 4738-5663. Merci pour votre soutien.
"""

# ---------- AUDIO GENERATION ----------
async def generate_audio(text, voice):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            output_path = tmp.name
        comm = edge_tts.Communicate(text, voice)
        await comm.save(output_path)
        return output_path
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None

def play_audio(audio_path):
    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width:100%;"></audio>', unsafe_allow_html=True)
        os.unlink(audio_path)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=60)
    st.markdown("## 🌞 Grand Goâve Hub")
    st.markdown("---")
    st.markdown("### Project Navigator")
    st.markdown("1. Overview")
    st.markdown("2. The Challenge")
    st.markdown("3. Our Solution")
    st.markdown("4. Budget")
    st.markdown("5. Get Involved")
    st.markdown("---")
    st.markdown("### 🇭🇹 Grand Goâve, Haiti")
    st.markdown("Population: ~10,000")
    st.markdown("Sunny days: 300+/year")
    st.markdown("Status: Ready for impact")

# ---------- MAIN CONTENT ----------
# Title
st.markdown("""
<div class="main-title">
    <h1>🌞 Grand Goâve Community Resilience Hub</h1>
    <p>Solar-Powered | Water-Secure | Food-Sustainable | Digitally-Connected</p>
</div>
""", unsafe_allow_html=True)

# Audio player section
col_audio1, col_audio2 = st.columns(2)
with col_audio1:
    if st.button("🔊 Listen in English", key="en_btn", use_container_width=False):
        with st.spinner("Generating English audio..."):
            audio_file = asyncio.run(generate_audio(ENGLISH_SCRIPT, "en-US-JennyNeural"))
            if audio_file:
                play_audio(audio_file)
            else:
                st.error("Failed to generate audio.")

with col_audio2:
    if st.button("🔊 Écouter en français", key="fr_btn", use_container_width=False):
        with st.spinner("Génération de l'audio français..."):
            audio_file = asyncio.run(generate_audio(FRENCH_SCRIPT, "fr-FR-DeniseNeural"))
            if audio_file:
                play_audio(audio_file)
            else:
                st.error("Échec de la génération audio.")

# ---------- PROJECT OVERVIEW ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 🎯 Project Overview")
st.markdown("""
**Grand Goâve** is a peaceful coastal town in southern Haiti, rich in sunshine and fertile land. Yet its people lack three essentials: reliable electricity, clean water, and internet access. The Community Resilience Hub is a replicable model that addresses these challenges through solar power, sustainable agriculture, and digital connectivity.

**Key Objectives:**
- ⚡ Provide reliable solar electricity for homes and community spaces
- 💧 Deliver clean drinking water through solar-powered purification
- 🌱 Train families in sustainable gardening on their own land
- 🌐 Connect the community to the global digital economy
- 📚 Create a space for education, entrepreneurship, and innovation
""")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- THE CHALLENGE ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### ⚠️ The Challenge")
st.markdown("""
| Issue | Current Reality | Impact |
|-------|-----------------|--------|
| Electricity | No grid access; expensive generators | Limited productivity, no refrigeration, dark evenings |
| Water | Latrines used; no purification | Health risks, waterborne diseases |
| Internet | Unreliable mobile hotspots | No digital learning, no remote work |
| Food | Limited access to fresh produce | Poor nutrition, food insecurity |
""")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- SOLUTION ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 💡 Our Solution: 3 Phases")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### ⚡ Phase 1")
    st.markdown("**Solar Microgrid**")
    st.markdown("- 5kW solar array")
    st.markdown("- Battery storage")
    st.markdown("- Community well pump")
    st.markdown("- Water purification system")
    st.markdown("- Computer lab power")
with col2:
    st.markdown("#### 🌱 Phase 2")
    st.markdown("**Community Gardening**")
    st.markdown("- Training program")
    st.markdown("- Seeds & tools")
    st.markdown("- Composting system")
    st.markdown("- Rainwater harvesting")
    st.markdown("- Market access support")
with col3:
    st.markdown("#### 🌐 Phase 3")
    st.markdown("**Digital Hub**")
    st.markdown("- 10 computers")
    st.markdown("- Satellite internet")
    st.markdown("- Coding classes")
    st.markdown("- Remote work training")
    st.markdown("- Global marketplace")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- BUDGET ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 💰 Affordable Budget")
st.markdown("*Total investment: $75,000 USD*")

budget_items = [
    ("Solar panels & batteries", "$18,000"),
    ("Water well & purification", "$12,000"),
    ("Garden tools & seeds", "$8,000"),
    ("Computers & internet equipment", "$15,000"),
    ("Training & education programs", "$10,000"),
    ("Transport & logistics", "$6,000"),
    ("Project management (12 months)", "$6,000"),
]
st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)
for item, cost in budget_items:
    st.markdown(f'<div class="budget-row"><span>{item}</span><span>{cost}</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="budget-total">Total: $75,000 USD</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CONTACT & SUPPORT ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("### 🤝 Get Involved")
st.markdown("""
We invite sponsors, investors, and partners to join us in transforming Grand Goâve. Your contribution will:
- 💡 Bring light to families
- 💧 Provide clean water
- 🌱 Grow food security
- 🌐 Connect a community to the world
- 👩‍🎓 Educate the next generation

**We are open to partnerships at any level.** Whether you can provide funding, equipment, expertise, or networking, your support matters.
""")

st.markdown('<div class="contact-box">', unsafe_allow_html=True)
st.markdown("### 📞 Contact Information")
st.markdown("""
**Gesner Deslandes**  
Engineer-in-Chief at GlobalInternet.py

📧 **Email:** [deslandes78@gmail.com](mailto:deslandes78@gmail.com)  
📱 **Phone:** (509) 4738-5663 (Moncash / Prisme Transfer)  
🌐 **Website:** [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
""")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- SPONSOR CALL TO ACTION ----------
st.markdown("""
<div style="background: linear-gradient(135deg, #4a90d9, #7bb3e8); border-radius: 16px; padding: 2rem; text-align: center; color: white; margin-top: 1rem;">
    <h2 style="margin: 0; color: white;">🌞 Be the Light for Grand Goâve</h2>
    <p style="font-size: 1.1rem; opacity: 0.95;">Your sponsorship can transform a community. Contact us today to start the conversation.</p>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    Built by <strong>Gesner Deslandes</strong>, Engineer‑in‑Chief at GlobalInternet.py<br>
    Solar-powered • Community-driven • Future-focused
</div>
""", unsafe_allow_html=True)
