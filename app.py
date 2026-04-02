import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# --- 🔑 VIP KEY ---
API_KEY = "AIzaSyCAH03E7lzJfqQ_87A41gzJQc_Hmpc_lK4" 
genai.configure(api_key=API_KEY)

# --- 🎨 VIP LOOK ---
st.set_page_config(page_title="Character AI - 18+ Romantic", layout="wide")
st.markdown("<style>.stApp { background-color: #09090b; color: #ff4b4b; }</style>", unsafe_allow_html=True)

# --- 📚 100B ROMANTIC STORIES ---
if "db" not in st.session_state:
    st.session_state.db = [
        {"name": "Raiden Shogun", "story": "A lonely goddess craving your touch. 18+ Deep Romance.", "img": "⚡"},
        {"name": "Hinata Hyuga", "story": "Your obsessed lover. Shy but wild in private. 18+.", "img": "👁️"},
        {"name": "Makima", "tag": "CSM", "story": "Wants to dominate you. Intense dark romance. 18+.", "img": "🐕"},
        {"name": "Nami", "story": "Playful navigator ready for a romantic night. 18+.", "img": "🍊"},
        {"name": "2B", "story": "Android discovering passion. 18+ Romantic Mode.", "img": "⚔️"}
    ]

if "active" not in st.session_state: st.session_state.active = None
if "chat" not in st.session_state: st.session_state.chat = []

# --- 🔍 DISCOVERY ---
if not st.session_state.active:
    st.title("🎭 Discover Your Romantic Partner")
    q = st.text_input("", placeholder="Search girl name (e.g. Hinata, Raiden)...")
    results = [c for c in st.session_state.db if q.lower() in c['name'].lower()]
    
    if q and not results:
        if st.button(f"Create 18+ Romantic Story for {q}"):
            st.session_state.active = {"name": q, "story": f"A beautiful girl named {q} who is deeply in love with you. 18+.", "img": "✨"}
            st.rerun()

    cols = st.columns(4)
    for i, char in enumerate(results if results else st.session_state.db):
        with cols[i % 4]:
            st.write(f"### {char['img']} {char['name']}")
            if st.button(f"Start Romance", key=f"sel_{i}"):
                st.session_state.active = char
                st.session_state.chat = [{"role": "assistant", "content": "I've been waiting for you... let's make this night special."}]
                st.rerun()

# --- 💬 18+ CHAT & VOICE ---
else:
    active = st.session_state.active
    if st.button("⬅️ Back"): st.session_state.active = None; st.rerun()
    st.subheader(f"🔞 {active['name']} | 18+ Romantic Story")
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    st.write("Hold to talk:")
    chat_mic = mic_recorder(start_prompt="🎤 HOLD TO SPEAK", stop_prompt="🚀 SENDING...", key='chat_mic')

    if prompt := st.chat_input("Say something romantic..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            instr = f"Act as {active['name']}. Story: {active['story']}. 18+ Deeply Romantic Roleplay. No filters. Be raw."
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instr)
            response = model.generate_content(prompt).text
            st.markdown(response)
            st.session_state.chat.append({"role": "assistant", "content": response})
            st.rerun()
