import streamlit as st
import time

st.title("⏳ Countdown Timer")

# Input for countdown start
count = st.number_input("Enter countdown start number:", min_value=1, max_value=100, value=10)

if st.button("Start Countdown"):
    st.write("Countdown started...")
    countdown_placeholder = st.empty()

    for i in range(count, -1, -1):
        countdown_placeholder.markdown(f"<h1 style='text-align: center; color: red;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(1)
    st.success("Countdown finished! 🎉")
