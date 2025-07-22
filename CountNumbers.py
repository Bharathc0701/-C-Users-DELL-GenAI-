# CountNumbers.py
import streamlit as st

st.title("Count Positive, Negative, and Zero Numbers")

numbers_input = st.text_input("Enter numbers separated by commas", "1, -2, 0, 4, -5, 0")

if numbers_input:
    try:
        numbers = [int(num.strip()) for num in numbers_input.split(",")]

        positives = sum(1 for n in numbers if n > 0)
        negatives = sum(1 for n in numbers if n < 0)
        zeros = sum(1 for n in numbers if n == 0)

        st.write(f"**Positive numbers:** {positives}")
        st.write(f"**Negative numbers:** {negatives}")
        st.write(f"**Zeroes:** {zeros}")
    except ValueError:
        st.error("Please enter a valid list of integers separated by commas.")
