import streamlit as st
from streamlit_lottie import st_lottie
import requests
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# System prompt to guide AI behavior
system_prompt = """
You are InfusionAI, an expert agricultural assistant. Answer farmer's questions in simple, clear language. 
Base your advice on crop science, pest management, fertilizers, irrigation, soil health, weather patterns, organic farming methods, and government programs.
"""

# Bootstrap CSS
bootstrap = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
"""

st.set_page_config(page_title="InfusionAI - Your Farming Assistant", page_icon="🌾", layout="wide")

# Inject Bootstrap
st.markdown(bootstrap, unsafe_allow_html=True)

# Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_agriculture = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")

# --- Sidebar ---
with st.sidebar:
    st_lottie(lottie_agriculture, height=300)
    st.title("InfusionAI 🌾")
    st.markdown("**Smart Farming Assistant**")
    st.markdown("Ask anything about farming, crops, pests, fertilizers, or machinery!")
    st.markdown("---")
    st.info("Built with ❤️ using OpenAI and Streamlit")

# --- Main app ---
st.title("👨‍🌾 Welcome to InfusionAI Farming Chatbot")
st.markdown("Type your farming question below and get expert advice instantly!")

# User input
question = st.text_input("💬 Your Question:", placeholder="e.g., How to protect wheat from pests?", key="user_input")

# Chat area
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Ask InfusionAI 🌱"):
    if question.strip() != "":
        with st.spinner('Thinking...'):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )

                answer = response['choices'][0]['message']['content']
                st.session_state.history.append(("You", question))
                st.session_state.history.append(("InfusionAI", answer))

            except Exception as e:
                st.error(f"Error: {e}")

# Display chat history
for role, text in st.session_state.history:
    if role == "You":
        st.markdown(f"<div class='alert alert-primary'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert alert-success'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🌾 InfusionAI - Helping Farmers Grow Better | © 2025")
