import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import subprocess, sys, os
import requests

st.markdown("<h1 style='text-align:center; color:#ff007f; font-size:40px;'>🌟 MADE BY ADITYA 🌟</h1>", unsafe_allow_html=True)
st.write("🔐 Tally Automation Subscription Portal (Streamlit)")

col1, col2 = st.columns(2)
with col1:
    if st.button("💸 ₹500 / Month"):
        st.session_state['plan'] = 'Monthly'
        st.session_state['show_qr'] = True
with col2:
    if st.button("💰 ₹5500 / Year"):
        st.session_state['plan'] = 'Yearly'
        st.session_state['show_qr'] = True

if 'show_qr' in st.session_state and st.session_state['show_qr']:
    st.info(f"📱 Scan this QR to pay for your **{st.session_state['plan']}** subscription.")
    qr_path = os.path.join(os.path.dirname(__file__), 'qr.png')
    try:
        image = Image.open(qr_path)
        st.image(image, caption="Scan & Pay using PhonePe / UPI")
    except Exception:
        st.text("QR image not found (place qr.png beside this script).")

    if st.button("✅ I have paid"):
        st.success("Thank you! Notifying dashboard to grant access...")
        # Call the Flask webhook to add this user's email (for demo we ask email)
        email = st.text_input("Enter your email to link access (same email for dashboard):")
        if st.button("Link Email & Grant Access"):
            payload = {"email": email, "plan": st.session_state.get('plan')}
            # Make a POST to the dashboard webhook (the dashboard must be public)
            try:
                webhook = st.text_input("Enter Dashboard webhook URL (e.g. https://your-app.onrender.com/payment_webhook)")
                resp = requests.post(webhook, json=payload)
                if resp.ok:
                    st.success("✅ Access request sent. Now login on Dashboard with same email.")
                else:
                    st.error(f"Webhook call failed: {resp.status_code}")
            except Exception as e:
                st.error(f"Failed: {e}")

if 'access_granted' in st.session_state and st.session_state['access_granted']:
    st.success("Access active.")
