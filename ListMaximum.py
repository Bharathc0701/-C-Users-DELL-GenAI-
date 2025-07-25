import streamlit as st

st.title("List Maximum Finder (No max function)")

# User inputs a list of numbers separated by commas
user_input = st.text_input("Enter a list of numbers separated by commas:")

def find_max(numbers):
    # Initialize the first number as the maximum
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

if user_input:
    try:
        # Convert input string to list of numbers
        number_list = [float(x.strip()) for x in user_input.split(',')]
        result = find_max(number_list)
        st.success(f"The largest number is: {result}")
    except ValueError:
        st.error("Please enter a valid list of numbers separated by commas.")
