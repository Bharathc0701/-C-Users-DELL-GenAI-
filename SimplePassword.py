# SimplePassword.py
import streamlit as st

st.title("🔐 Simple Password Checker")

password = st.text_input("Enter your password:", type="password")

min_length = 8

if password:
    if len(password) >= min_length:
        st.success("✅ Password is strong enough!")
    else:
        st.error(f"❌ Password too short! It must be at least {min_length} characters long.")
