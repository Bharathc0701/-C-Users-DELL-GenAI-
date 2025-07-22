import streamlit as st

# App Title
st.title("Age Category Checker")

# Input from user
age = st.number_input("Enter your age", min_value=0, step=1)

# Function to determine category
def get_age_category(age):
    if age < 13:
        return "Child"
    elif age < 20:
        return "Teenager"
    elif age < 60:
        return "Adult"
    else:
        return "Senior"

# Show result when button is clicked
if st.button("Check Category"):
    category = get_age_category(age)
    st.success(f"You are categorized as: **{category}**")
