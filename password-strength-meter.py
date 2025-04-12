import re
import streamlit as st
 
st.set_page_config(page_title="Password Strength Checker", page_icon="🔒", layout="centered")
 
st.markdown("""
<style>
    /* Center the main container content */
    .main {
        text-align: center;
    }
    .stTextInput> input {
        width: 60% !important;
        margin: auto;
    }
    .stButton>button {
        width: 60%;
        height: 50px;
        background-color: #87CEFA;  
        color: white;
        font-size: 18px;
        border: none;
        border-radius: 5px;
        display: block;
        margin: 20px auto;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4682B4;  
    }
    .feedback {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Password Strength Checker")
st.write("Enter your password to check its security level.")

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", 
    "letmein", "monkey", "111111", "123123", "welcome"
}

def check_password_strength(password):
    feedback = []
    score = 0
    max_score = 6  

  
    if len(password) >= 8:
        score += 1
        if len(password) >= 12:
            score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
 
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
 
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*(),.?\":{}|<>).")
 
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("❌ This is a very common password. Please choose something more unique.")
        score = 0  

    if score >= 6:
        strength_message = "✅ Very Strong Password!"
    elif score >= 4:
        strength_message = "⚠️ Moderate Password - Consider adding more security features."
    else:
        strength_message = "❌ Weak Password - Improve it using the suggestions above."

    strength_percent = int((score / max_score) * 100)
    
    return strength_message, feedback, strength_percent

password = st.text_input("Enter your password:", type="password")

if st.button("Check Password Strength"):
    if password:
        strength_message, suggestions, strength_percent = check_password_strength(password)
        
        st.markdown(f"### Strength: {strength_message}")
        st.progress(strength_percent)
        
        if suggestions:
            st.markdown("#### Suggestions to improve your password:")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
    else:
        st.error("Please enter a password to check.")
