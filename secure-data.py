import streamlit as st
import hashlib
import base64
import json
import time
import os
import random
import string

# Check if cryptography is available, otherwise use a simpler encryption
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

# Session state initialization
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}  # {"user1_data": {"encrypted_text": "xyz", "passkey": "hashed"}}
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'last_failed_time' not in st.session_state:
    st.session_state.last_failed_time = 0
if 'locked_out' not in st.session_state:
    st.session_state.locked_out = False
if 'cipher_key' not in st.session_state and CRYPTOGRAPHY_AVAILABLE:
    # Generate a key (this should be stored securely in production)
    st.session_state.cipher_key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.cipher_key)

# Constants
LOCKOUT_DURATION = 30  # seconds
MAX_ATTEMPTS = 3
MASTER_PASSWORD = "admin123"  # In a real app, this would be stored more securely

# Simple Caesar cipher for fallback encryption when cryptography is not available
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Function to generate a pseudo-random string for the ID
def generate_id(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text, passkey):
    if CRYPTOGRAPHY_AVAILABLE:
        key = generate_key_from_passkey(passkey)
        cipher = Fernet(key)
        return cipher.encrypt(text.encode()).decode()
    else:
        # Fallback to Caesar cipher with a shift derived from the passkey
        shift = sum(ord(c) for c in passkey) % 26
        encrypted = caesar_encrypt(text, shift)
        # Create a unique ID for this encrypted text
        unique_id = generate_id()
        return f"{unique_id}:{encrypted}"

# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    try:
        if CRYPTOGRAPHY_AVAILABLE:
            key = generate_key_from_passkey(passkey)
            cipher = Fernet(key)
            return cipher.decrypt(encrypted_text.encode()).decode()
        else:
            # Parse the unique ID and encrypted text
            if ":" not in encrypted_text:
                return None
            unique_id, encrypted = encrypted_text.split(":", 1)
            shift = sum(ord(c) for c in passkey) % 26
            return caesar_decrypt(encrypted, shift)
    except Exception:
        return None

# Function to generate key from passkey (only if cryptography is available)
def generate_key_from_passkey(passkey, salt=b'salt_'):
    if CRYPTOGRAPHY_AVAILABLE:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(passkey.encode()))
        return key
    return None

# Function to verify passkey
def verify_passkey(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)
    
    if encrypted_text in st.session_state.stored_data:
        if st.session_state.stored_data[encrypted_text]["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return True
    
    st.session_state.failed_attempts += 1
    st.session_state.last_failed_time = time.time()
    
    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
        st.session_state.locked_out = True
    
    return False

# Function to check lockout status
def check_lockout():
    if st.session_state.locked_out:
        time_passed = time.time() - st.session_state.last_failed_time
        if time_passed >= LOCKOUT_DURATION:
            st.session_state.locked_out = False
            return False
        return True
    return False

# Function to save data to JSON file (for persistence)
def save_data_to_file():
    with open('encrypted_data.json', 'w') as f:
        json.dump(st.session_state.stored_data, f)

# Function to load data from JSON file
def load_data_from_file():
    try:
        with open('encrypted_data.json', 'r') as f:
            st.session_state.stored_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.stored_data = {}

# Try to load data at startup
try:
    load_data_from_file()
except Exception:
    pass

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Display cryptography status
if not CRYPTOGRAPHY_AVAILABLE:
    st.warning("⚠️ The 'cryptography' package is not installed. Using simplified encryption instead. For better security, install the package with: `pip install cryptography`")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

# Check for lockout and redirect if needed
if check_lockout() and choice != "Login":
    st.warning("🔒 Account locked due to too many failed attempts! Please reauthorize.")
    choice = "Login"

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    
    st.info("This system uses:")
    if CRYPTOGRAPHY_AVAILABLE:
        st.markdown("""
        - **PBKDF2** for secure key derivation
        - **Fernet symmetric encryption** for data security
        - **SHA-256** for passkey hashing
        - **In-memory storage** with optional JSON persistence
        """)
    else:
        st.markdown("""
        - **Caesar cipher** for basic encryption (simplified)
        - **SHA-256** for passkey hashing
        - **In-memory storage** with optional JSON persistence
        """)
    
    st.warning("⚠️ Remember your passkeys! There's no way to recover your data if you forget them.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    
    user_data = st.text_area("Enter Data to Encrypt:", height=150)
    passkey = st.text_input("Create Passkey:", type="password")
    confirm_passkey = st.text_input("Confirm Passkey:", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        store_button = st.button("Encrypt & Save", type="primary")
    
    with col2:
        persist = st.checkbox("Save to file (persistence)")
    
    if store_button:
        if not user_data:
            st.error("⚠️ Please enter data to encrypt!")
        elif not passkey:
            st.error("⚠️ Please create a passkey!")
        elif passkey != confirm_passkey:
            st.error("⚠️ Passkeys don't match!")
        else:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data, passkey)
            
            # Store the data
            st.session_state.stored_data[encrypted_text] = {
                "encrypted_text": encrypted_text, 
                "passkey": hashed_passkey,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if persist:
                save_data_to_file()
            
            st.success("✅ Data encrypted and stored successfully!")
            st.code(encrypted_text, language=None)
            st.info("📌 Copy this encrypted text - you'll need it to retrieve your data later.")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")
    
    if st.button("Decrypt", type="primary"):
        if not encrypted_text:
            st.error("⚠️ Please enter the encrypted data!")
        elif not passkey:
            st.error("⚠️ Please enter your passkey!")
        else:
            # Check if the encrypted text exists in storage
            if encrypted_text in st.session_state.stored_data:
                if verify_passkey(encrypted_text, passkey):
                    decrypted_text = decrypt_data(encrypted_text, passkey)
                    if decrypted_text:
                        st.success("✅ Data decrypted successfully!")
                        st.markdown("### Decrypted Content:")
                        st.markdown(f"```\n{decrypted_text}\n```")
                    else:
                        st.error("❌ Decryption failed. Invalid passkey!")
                else:
                    remaining = MAX_ATTEMPTS - st.session_state.failed_attempts
                    if remaining > 0:
                        st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")
                    else:
                        st.error("❌ Too many failed attempts! Account locked.")
                        st.warning("🔒 Redirecting to login page...")
                        time.sleep(1)
                        st.experimental_rerun()
            else:
                st.error("❌ No such encrypted data found in storage!")
    
    # Display attempts warning if needed
    if st.session_state.failed_attempts > 0 and st.session_state.failed_attempts < MAX_ATTEMPTS:
        st.warning(f"⚠️ Failed attempts: {st.session_state.failed_attempts}/{MAX_ATTEMPTS}")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    
    if check_lockout():
        time_passed = time.time() - st.session_state.last_failed_time
        time_remaining = max(0, LOCKOUT_DURATION - time_passed)
        
        st.error(f"🔒 Account locked due to too many failed attempts!")
        st.warning(f"Please wait {int(time_remaining)} seconds before trying again.")
        
        # Auto refresh when lockout period is over
        if time_remaining <= 0.5:
            st.session_state.locked_out = False
            st.experimental_rerun()
    else:
        login_pass = st.text_input("Enter Master Password:", type="password")
        
        if st.button("Login", type="primary"):
            if login_pass == MASTER_PASSWORD:
                st.session_state.failed_attempts = 0
                st.session_state.locked_out = False
                st.success("✅ Reauthorized successfully!")
                
                with st.spinner("Redirecting to Home..."):
                    time.sleep(1)
                    st.experimental_rerun()
            else:
                st.error("❌ Incorrect master password!")

# Display data statistics in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📊 System Stats")
st.sidebar.info(f"Stored Items: {len(st.session_state.stored_data)}")

# Add footer
st.sidebar.markdown("---")
st.sidebar.caption("Secure Data Encryption System v1.0")
st.sidebar.caption("Built with Streamlit")
# Add footer
st.sidebar.markdown("---")
st.sidebar.caption("Secure Data Encryption System v1.0")
st.sidebar.caption("Built with Streamlit & Cryptography")