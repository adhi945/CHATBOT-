import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import requests
from streamlit_lottie import st_lottie

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Bootstrap CSS
bootstrap = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
"""

# Streamlit page setup
st.set_page_config(page_title="InfusionAI - Your Farming Assistant", page_icon="🌾", layout="wide")

# Inject Bootstrap
st.markdown(bootstrap, unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_agriculture = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")

# Sidebar
with st.sidebar:
    st_lottie(lottie_agriculture, height=300)
    st.title("InfusionAI 🌾")
    st.markdown("**Smart Farming Assistant**")
    st.markdown("Ask anything about farming, crops, pests, fertilizers, or machinery!")
    st.markdown("---")
    st.info("Built with ❤️ using Groq + Llama 3 + Streamlit")

# System prompt for the chatbot
system_prompt = """
You are InfusionAI, an expert agricultural assistant. 
Your mission is to give simple, clear, and actionable farming advice to any question. 
Use your expertise in crops, soil, fertilizers, pests, weather patterns, organic farming, machinery, and government policies.
Answer in a helpful and friendly manner.
"""

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Main Title
st.title("👨‍🌾 Welcome to InfusionAI Farming Chatbot")

st.markdown("Type your farming question below and get expert advice instantly!")

# User input
question = st.text_input("💬 Your Farming Question:")

# Button to ask
if st.button("Ask InfusionAI 🌱"):
    if question.strip() != "":
        with st.spinner('Thinking... 🌾'):
            try:
                response = client.chat.completions.create(
                    model="llama3-70b-8192",  # Powerful model!
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                answer = response.choices[0].message.content

                # Save history
                st.session_state.history.append(("You", question))
                st.session_state.history.append(("InfusionAI", answer))

            except Exception as e:
                st.error(f"Error: {e}")

# Display Chat History
for role, text in st.session_state.history:
    if role == "You":
        st.markdown(f"<div class='alert alert-primary'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='alert alert-success'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🌾 InfusionAI - Helping Farmers Grow Better | Powered by Groq & Llama3 | © 2025")
