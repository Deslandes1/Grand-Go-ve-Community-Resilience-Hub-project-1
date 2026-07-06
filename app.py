import streamlit as st
import asyncio
import tempfile
import os
import base64
import re
import subprocess
import time

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
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR CONTENT (also used for narration) ----------
sidebar_text = """
Grand Goâve Hub – Project Navigator. The sidebar contains the following sections: Overview, The Challenge, Our Solution, Budget, and Get Involved. Grand Goâve, Haiti – population about ten thousand, sunny days over three hundred per year, and the community is ready for impact.
"""

# ---------- FULL NARRATION SCRIPTS ----------
ENGLISH_SCRIPT = """
Grand Goâve Community Resilience Hub. Solar-Powered, Water-Secure, Food-Sustainable, Digitally-Connected.

Project Overview. Grand Goâve is a peaceful coastal town in southern Haiti, rich in sunshine and fertile land. Yet its people lack three essentials: reliable electricity, clean water, and internet access. The Community Resilience Hub is a replicable model that addresses these challenges through solar power, sustainable agriculture, and digital connectivity.

The key objectives are: provide reliable solar electricity for homes and community spaces. Deliver clean drinking water through solar-powered purification. Train families in sustainable gardening on their own land. Connect the community to the global digital economy. Create a space for education, entrepreneurship, and innovation.

The Challenge. Currently, there is no grid access, and generators are expensive, limiting productivity and refrigeration. Water sources are unsafe, with latrines still in use, causing health risks. Internet access is unreliable, preventing digital learning and remote work. Food insecurity is high due to limited access to fresh produce.

Our Solution in Three Phases. Phase One: Solar Microgrid. This includes a five-kilowatt solar array, battery storage, a community well pump, water purification system, and power for a computer lab. Phase Two: Community Gardening. This provides training programs, seeds, tools, composting systems, rainwater harvesting, and market access support. Phase Three: Digital Hub. This includes ten computers, satellite internet, coding classes, remote work training, and access to the global marketplace.

The affordable budget totals seventy-five thousand US dollars. Breakdown: solar panels and batteries, eighteen thousand. Water well and purification, twelve thousand. Garden tools and seeds, eight thousand. Computers and internet equipment, fifteen thousand. Training and education programs, ten thousand. Transport and logistics, six thousand. Project management for twelve months, six thousand. Total investment: seventy-five thousand US dollars.

Get Involved. We invite sponsors, investors, and partners to join us in transforming Grand Goâve. Your contribution will bring light to families, provide clean water, grow food security, connect a community to the world, and educate the next generation. We are open to partnerships at any level. Whether you can provide funding, equipment, expertise, or networking, your support matters.

Contact Information. Gesner Deslandes, Engineer-in-Chief at GlobalInternet.py. Email: deslandes78@gmail.com. Phone: (509) 4738-5663. Website: globalinternetsitepy.streamlit.app.

Be the Light for Grand Goâve. Your sponsorship can transform a community. Contact us today to start the conversation.

Built by Gesner Deslandes, Engineer-in-Chief at GlobalInternet.py. Solar-powered, Community-driven, Future-focused.

Now, let's look at the sidebar. The sidebar contains the project navigator with sections: Overview, The Challenge, Our Solution, Budget, and Get Involved. It also shows that Grand Goâve, Haiti, has a population of about ten thousand, over three hundred sunny days per year, and is ready for impact.

Conclusion. How is this project possible? It is possible because we combine proven technologies with local knowledge and community participation. The abundant sunshine provides free energy. The fertile land can grow food. The people have the will and the skills to make it work. With the right partnership and modest investment, we can turn this vision into reality. We invite all sponsors to visit the live demo of this project at the following link: https://grand-goave-community-hub.streamlit.app to see the full proposal and interactive budget breakdown. Together, we can build resilience, dignity, and hope. Thank you for your support.
"""

FRENCH_SCRIPT = """
Projet Hub de Résilience Communautaire de Grand Goâve. Solaire, Sécurité d'eau, Alimentation durable, Connecté numériquement.

Aperçu du projet. Grand Goâve est une ville côtière paisible du sud d'Haïti, riche en soleil et en terres fertiles. Pourtant, ses habitants manquent de trois éléments essentiels : électricité fiable, eau potable et accès à Internet. Le Hub de Résilience Communautaire est un modèle reproductible qui relève ces défis grâce à l'énergie solaire, l'agriculture durable et la connectivité numérique.

Les objectifs clés sont : fournir de l'électricité solaire fiable pour les maisons et les espaces communautaires. Distribuer de l'eau potable via une purification solaire. Former les familles au jardinage durable sur leurs propres terres. Connecter la communauté à l'économie numérique mondiale. Créer un espace pour l'éducation, l'entrepreneuriat et l'innovation.

Le défi. Actuellement, il n'y a pas d'accès au réseau électrique, les générateurs sont chers, limitant la productivité et la réfrigération. Les sources d'eau sont dangereuses, avec des latrines encore utilisées, causant des risques sanitaires. L'accès à Internet est peu fiable, empêchant l'apprentissage numérique et le travail à distance. L'insécurité alimentaire est élevée en raison d'un accès limité aux produits frais.

Notre solution en trois phases. Phase un : micro-réseau solaire. Cela comprend un panneau solaire de cinq kilowatts, des batteries, une pompe de puits communautaire, un système de purification d'eau et l'alimentation d'un laboratoire informatique. Phase deux : jardinage communautaire. Cela offre des programmes de formation, des semences, des outils, des systèmes de compostage, la récupération d'eau de pluie et un soutien à l'accès au marché. Phase trois : hub numérique. Cela comprend dix ordinateurs, un accès Internet par satellite, des cours de codage, une formation au travail à distance et un accès au marché mondial.

Le budget abordable totalise soixante-quinze mille dollars américains. Détails : panneaux solaires et batteries, dix-huit mille. Puits et purification d'eau, douze mille. Outils et semences de jardin, huit mille. Ordinateurs et équipements Internet, quinze mille. Formation et programmes éducatifs, dix mille. Transport et logistique, six mille. Gestion de projet pendant douze mois, six mille. Investissement total : soixante-quinze mille dollars américains.

Participez. Nous invitons les sponsors, investisseurs et partenaires à se joindre à nous pour transformer Grand Goâve. Votre contribution apportera la lumière aux familles, fournira de l'eau potable, améliorera la sécurité alimentaire, connectera la communauté au monde et éduquera la prochaine génération. Nous sommes ouverts aux partenariats à tous les niveaux. Que vous puissiez fournir du financement, de l'équipement, de l'expertise ou du réseautage, votre soutien est important.

Coordonnées. Gesner Deslandes, ingénieur en chef chez GlobalInternet.py. Email : deslandes78@gmail.com. Téléphone : (509) 4738-5663. Site web : globalinternetsitepy.streamlit.app.

Soyez la lumière pour Grand Goâve. Votre parrainage peut transformer une communauté. Contactez-nous dès aujourd'hui pour lancer la conversation.

Construit par Gesner Deslandes, ingénieur en chef chez GlobalInternet.py. Solaire, communautaire, tourné vers l'avenir.

Parlons maintenant de la barre latérale. La barre latérale contient le navigateur de projet avec les sections : Aperçu, Le défi, Notre solution, Budget et Participez. Elle indique également que Grand Goâve, Haïti, a une population d'environ dix mille habitants, plus de trois cents jours d'ensoleillement par an, et est prête pour l'impact.

Conclusion. Comment ce projet est-il possible ? Il est possible parce que nous combinons des technologies éprouvées avec les connaissances locales et la participation communautaire. Le soleil abondant fournit de l'énergie gratuite. La terre fertile peut produire de la nourriture. Les gens ont la volonté et les compétences pour le faire fonctionner. Avec le bon partenariat et un investissement modeste, nous pouvons transformer cette vision en réalité. Nous invitons tous les sponsors à visiter la démo en direct de ce projet à l'adresse suivante : https://grand-goave-community-hub.streamlit.app pour voir la proposition complète et le budget interactif. Ensemble, nous pouvons bâtir la résilience, la dignité et l'espoir. Merci pour votre soutien.
"""

# ---------- CHUNKING FUNCTION ----------
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
    # If a single chunk is still too long, split by words
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
        # First, try to generate the entire text at once
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                output_path = tmp.name
            comm = edge_tts.Communicate(text, voice)
            await comm.save(output_path)
            if os.path.getsize(output_path) > 0:
                return output_path
        except Exception as e:
            st.warning(f"Full text generation failed ({e}). Trying chunked fallback...")

        # If that fails, split into chunks and concatenate using ffmpeg (if available)
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

        # Check if ffmpeg is available
        ffmpeg_available = False
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            ffmpeg_available = True
        except:
            ffmpeg_available = False

        if ffmpeg_available and len(temp_files) > 1:
            # Concatenate with ffmpeg
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
            # If only one chunk or ffmpeg not available, return the first chunk (or we could play sequentially)
            if len(temp_files) == 1:
                return temp_files[0]
            else:
                # Return a list of files to play sequentially (we'll handle in play_audio)
                return temp_files
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None

def play_audio(audio_files):
    if isinstance(audio_files, list):
        # Play sequentially using HTML5 audio with JavaScript
        if not audio_files:
            return
        # Build HTML with multiple audio elements and a script to play them in sequence
        html = """
        <div id="audio-container"></div>
        <script>
        (function() {
            const container = document.getElementById('audio-container');
            const audioSources = [];
        """
        for i, path in enumerate(audio_files):
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
        # Clean up files after playing? We'll clean up later.
        # For now, we leave them; they will be deleted when script ends.
    else:
        # Single file
        if audio_files and os.path.exists(audio_files):
            with open(audio_files, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width:100%;"></audio>', unsafe_allow_html=True)
            os.unlink(audio_files)

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
            audio_files = asyncio.run(generate_audio(ENGLISH_SCRIPT, "en-US-JennyNeural"))
            if audio_files:
                play_audio(audio_files)
            else:
                st.error("Failed to generate audio.")

with col_audio2:
    if st.button("🔊 Écouter en français", key="fr_btn", use_container_width=False):
        with st.spinner("Génération de l'audio français..."):
            audio_files = asyncio.run(generate_audio(FRENCH_SCRIPT, "fr-FR-DeniseNeural"))
            if audio_files:
                play_audio(audio_files)
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
