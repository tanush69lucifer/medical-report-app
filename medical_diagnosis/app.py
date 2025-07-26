import os
import streamlit as st
import base64
from PIL import Image
from ocr_utils import extract_text
from parser import extract_values
from modules.rule_based_engine import interpret_results
from modules.pdf_exporter import export_to_pdf

# ✅ Load Local CSS
def local_css(file_name):
    css_path = os.path.join("static", file_name)
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ✅ Page Config
st.set_page_config(page_title="Diagnostics Assistant", layout="centered")

# ✅ Display Centered MEDONOSIS and tagline
medonosis_logo = os.path.join("static", "MEDONOSIS.png")
tagline_logo = os.path.join("static", "Decode-Diagnose-Deliver.png")

st.image(Image.open(medonosis_logo), width=300, use_column_width=False)
st.image(Image.open(tagline_logo), width=350, use_column_width=False)

# ✅ Patient Info
st.subheader("👤 Patient Information")
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=1, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
conditions = st.text_area("Known Conditions")
date = st.date_input("Report Date")

# ✅ Upload Report
st.subheader("📑 Upload Report Image")
uploaded_files = st.file_uploader("Upload", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    all_reports = []
    for file in uploaded_files:
        temp_path = f"temp_{file.name}"
        with open(temp_path, "wb") as f:
            f.write(file.read())

        text = extract_text(temp_path)
        values = extract_values(text)
        all_reports.append(values)
        os.remove(temp_path)

    st.markdown("### 🧾 Extracted Values")
    for i, report in enumerate(all_reports):
        st.json(report)

    if st.button("🧠 Diagnose & Generate PDF"):
        summary = interpret_results(all_reports, age=age, gender=gender, conditions=conditions)

        st.markdown("### 🩺 AI Diagnosis Summary")
        safe_summary = summary.replace('\n', '<br>')
        st.markdown(f"""
        <div style='background-color:#e8f0fe; padding:15px; border-radius:10px; font-family:Segoe UI; color:#000; text-align:center;'>
            {safe_summary}
        </div>
        """, unsafe_allow_html=True)

        # ✅ Generate PDF with QR
        pdf_buffer, app_url, qr_path = export_to_pdf(name, age, gender, all_reports, summary)

        # ✅ Download Button
        st.markdown("### 📥 Download Report")
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name="report.pdf",
            mime="application/pdf"
        )

        # ✅ Show QR Code
        if os.path.exists(qr_path):
            st.image(qr_path, caption="📲 Scan to Open Diagnostics Assistant")

        # ✅ App Link
        st.markdown(f"🔗 [Visit Diagnostics Assistant]({app_url})", unsafe_allow_html=True)
