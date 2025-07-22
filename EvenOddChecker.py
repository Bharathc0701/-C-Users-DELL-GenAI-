# EvenOddChecker.py

import streamlit as st

st.title("🔢 Even or Odd Checker")

# Single number check
st.header("Check a Single Number")
num = st.number_input("Enter a number", step=1)

if st.button("Check Even/Odd"):
    if num % 2 == 0:
        st.success(f"{int(num)} is Even")
    else:
        st.error(f"{int(num)} is Odd")

# List of numbers check
st.header("Check a List of Numbers")
input_list = st.text_input("Enter numbers separated by commas (e.g., 2, 3, 7, 10)")

if st.button("Check List"):
    try:
        numbers = [int(x.strip()) for x in input_list.split(',')]
        results = {num: ("Even" if num % 2 == 0 else "Odd") for num in numbers}
        st.write("Results:")
        for num, status in results.items():
            st.write(f"{num} is {status}")
    except ValueError:
        st.warning("Please enter only valid integers separated by commas.")
