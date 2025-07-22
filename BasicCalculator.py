import streamlit as st

# Title
st.title("🧮 Basic Calculator")

# Input fields for two numbers
num1 = st.number_input("Enter first number", format="%.2f")
num2 = st.number_input("Enter second number", format="%.2f")

# Select operation
operation = st.selectbox("Choose operation", ("Add (+)", "Subtract (-)", "Multiply (*)", "Divide (/)"))

# Calculate based on selection
if st.button("Calculate"):
    if operation == "Add (+)":
        result = num1 + num2
        st.success(f"Result: {result}")
    elif operation == "Subtract (-)":
        result = num1 - num2
        st.success(f"Result: {result}")
    elif operation == "Multiply (*)":
        result = num1 * num2
        st.success(f"Result: {result}")
    elif operation == "Divide (/)":
        if num2 != 0:
            result = num1 / num2
            st.success(f"Result: {result}")
        else:
            st.error("Cannot divide by zero.")