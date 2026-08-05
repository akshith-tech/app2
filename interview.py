import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(page_title="Technical Interviewer Bot", layout="centered")
st.title("🤖 Technical Interview Pro")

# --- INITIALIZATION ---
# Using OpenRouter as the provider
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="ENTER_OPENAI_KEY",
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

# Sidebar for Instructions
with st.sidebar:
    st.header("Help & Instructions")
    st.markdown("""
    1. Fill out your candidate profile.
    2. Click **'Start Interview'**.
    3. The bot will ask one question at a time.
    4. Provide your code or explanation in the chat.
    ---
    *Status: Connected to OpenRouter*
    """)

# --- SETUP FORM ---
if not st.session_state.interview_started:
    with st.form("setup_form"):
        st.subheader("Candidate Profile")
        lang = st.selectbox("Programming Language", ["Python", "Java", "C++", "JavaScript"])
        level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        role = st.text_input("Target Role", value="Software Engineer")
        topics = st.text_input("Focus Topics", value="DSA, OOP, System Design")
        
        submitted = st.form_submit_button("Start Interview")
        if submitted:
            st.session_state.interview_started = True
            # Set the System Prompt defining the AI behavior
            sys_prompt = f"""
            You are an expert Technical Interviewer with experience at top tech companies.
            Context: Role is {role}, Level is {level}, Language is {lang}, Topics focus on {topics}.
            
            Strict Operational Rules:
            1. Ask ONLY ONE question at a time.
            2. Focus primarily on Data Structures and Algorithms (DSA) unless specified.
            3. After each user answer, provide constructive feedback on:
               - Correctness
               - Time/Space Complexity (Big O)
               - Code Quality
            4. If the user is stuck, provide gradual hints.
            5. Once the interview concludes, provide a summary of Strengths, Weaknesses, and a Roadmap.
            """
            st.session_state.messages.append({"role": "system", "content": sys_prompt})
            st.session_state.messages.append({"role": "assistant", "content": f"Hello! I am your interviewer today. I've reviewed your profile for the {role} position. We will be using {lang} to work through some {topics} challenges. Are you ready for the first question?"})
            st.rerun()

# --- INTERVIEW CHAT ---
if st.session_state.interview_started:
    # Display Chat History
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User Input Logic
    if prompt := st.chat_input("Enter your response or code here..."):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            try:
                # Note: Using 'openai/gpt-3.5-turbo' or 'google/gemini-2.0-flash-001' 
                # as a common model choice on OpenRouter.
                response = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001", 
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error connecting to OpenRouter: {e}")
