import streamlit as st

# Title
st.title("🔢 Number Comparison App")

# Input fields
num1 = st.number_input("Enter the first number", format="%.2f")
num2 = st.number_input("Enter the second number", format="%.2f")

# Compare when user clicks button
if st.button("Compare"):
    if num1 > num2:
        st.success(f"{num1} is greater than {num2}")
    elif num1 < num2:
        st.warning(f"{num1} is less than {num2}")
    else:
        st.info(f"Both numbers are equal: {num1}")
