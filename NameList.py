import streamlit as st

st.title("Enter 5 Names and See Their Lengths")

# Create input fields for 5 names
name1 = st.text_input("Enter Name 1")
name2 = st.text_input("Enter Name 2")
name3 = st.text_input("Enter Name 3")
name4 = st.text_input("Enter Name 4")
name5 = st.text_input("Enter Name 5")

# Store the names in a list
names = [name1, name2, name3, name4, name5]

# Only show result when all fields are filled
if all(names):
    st.subheader("Names and Their Lengths:")
    for name in names:
        st.write(f"{name} - {len(name)} characters")
else:
    st.info("Please enter all five names to see the results.")
