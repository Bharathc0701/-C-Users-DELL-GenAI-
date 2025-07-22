import streamlit as st

# Title of the app
st.title("👋 Personal Greeting App")

# Input from user
name = st.text_input("What is your name?")
age = st.number_input("What is your age?", min_value=1, max_value=120, step=1)
color = st.color_picker("Pick your favorite color")

# Generate greeting message
if st.button("Generate Greeting"):
    if name and age:
        st.markdown(f"### 🎉 Hello, {name}!")
        st.markdown(f"You're **{age} years old**, and your favorite color is:")
        st.markdown(f"<div style='width:100px;height:50px;background-color:{color};border-radius:10px;'></div>", unsafe_allow_html=True)
        st.success(f"Nice to meet you, {name}! Have a colorful day! 🌈")
    else:
        st.warning("Please enter both your name and age.")

# Footer
st.caption("🔁 Powered by Streamlit | AI-generated Code")