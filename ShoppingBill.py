import streamlit as st

st.title("🛒 Shopping Bill Calculator")

st.subheader("Enter details of 3 items:")

# Item 1
item1_price = st.number_input("Item 1 Price (₹)", min_value=0.0, format="%.2f")
item1_qty = st.number_input("Item 1 Quantity", min_value=0, step=1)

# Item 2
item2_price = st.number_input("Item 2 Price (₹)", min_value=0.0, format="%.2f")
item2_qty = st.number_input("Item 2 Quantity", min_value=0, step=1)

# Item 3
item3_price = st.number_input("Item 3 Price (₹)", min_value=0.0, format="%.2f")
item3_qty = st.number_input("Item 3 Quantity", min_value=0, step=1)

# Tax percentage
tax_percent = st.slider("Tax Percentage (%)", min_value=0, max_value=50, value=5)

if st.button("Calculate Bill"):
    subtotal = (item1_price * item1_qty) + (item2_price * item2_qty) + (item3_price * item3_qty)
    tax_amount = subtotal * (tax_percent / 100)
    total = subtotal + tax_amount

    st.success(f"Subtotal: ₹{subtotal:.2f}")
    st.info(f"Tax (@{tax_percent}%): ₹{tax_amount:.2f}")
    st.success(f"Total Amount Payable: ₹{total:.2f}")
