import streamlit as st

st.title("🎓 Grade Average Calculator")

st.write("Enter the scores for 5 tests to calculate the average and determine pass/fail status.")

# Input fields for scores
score1 = st.number_input("Test Score 1", min_value=0.0, max_value=100.0, step=0.1)
score2 = st.number_input("Test Score 2", min_value=0.0, max_value=100.0, step=0.1)
score3 = st.number_input("Test Score 3", min_value=0.0, max_value=100.0, step=0.1)
score4 = st.number_input("Test Score 4", min_value=0.0, max_value=100.0, step=0.1)
score5 = st.number_input("Test Score 5", min_value=0.0, max_value=100.0, step=0.1)

# Button to calculate average
if st.button("Calculate Average"):
    average = (score1 + score2 + score3 + score4 + score5) / 5
    st.success(f"Average Score: {average:.2f}")

    # Determine pass/fail (pass if average >= 50)
    if average >= 50:
        st.markdown("✅ **Result: PASS**")
    else:
        st.markdown("❌ **Result: FAIL**")
