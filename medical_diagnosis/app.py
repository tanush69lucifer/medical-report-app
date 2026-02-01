import os
import sys
import streamlit as st
import base64
from PIL import Image

# --- Add current folder to Python path so modules can be found ---
sys.path.append(os.path.dirname(__file__))

# --- OCR + Lab Report imports ---
from ocr_utils import extract_text
from parser import extract_values
from modules.rule_based_engine import interpret_results
from modules.pdf_exporter import export_to_pdf

# --- Deep Learning Models (fixed relative import) ---
from modules.deep_models import xray_model, ct_mri_model, ultrasound_model, utils_preprocess

# ✅ Load Local CSS
def local_css(file_name):
    css_path = os.path.join("static", file_name)
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ✅ Page Config
st.set_page_config(page_title="Diagnostics Assistant", layout="centered")

# ✅ Display Logos
logo1_path = os.path.join(os.path.dirname(__file__), "static", "MEDONOSIS.png")
logo2_path = os.path.join(os.path.dirname(__file__), "static", "Decode-Diagnose-Deliver.png")

col1, col2 = st.columns([1, 1])
with col1:
    st.image(Image.open(logo1_path), width=300)
with col2:
    st.image(Image.open(logo2_path), width=350)

# ====================================
# 📌 MODE SELECTION
# ====================================
mode = st.radio("Choose Diagnosis Mode:", ["Lab Report (OCR)", "Medical Imaging"])

# ====================================
# 📑 LAB REPORT (OCR)
# ====================================
if mode == "Lab Report (OCR)":
    st.subheader("👤 Patient Information")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    conditions = st.text_area("Known Conditions")
    date = st.date_input("Report Date")

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
            <div style='background-color:#e8f0fe; padding:15px; border-radius:10px; font-family:Segoe UI; color:#000; text-align:center;'>{safe_summary}</div>
            """, unsafe_allow_html=True)

            pdf_buffer, app_url, qr_path = export_to_pdf(name, age, gender, all_reports, summary)

            st.markdown("### 📥 Download Report")
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name="report.pdf",
                mime="application/pdf"
            )

            if os.path.exists(qr_path):
                st.image(qr_path, caption="📲 Scan to Open Diagnostics Assistant")

            st.markdown(f"🔗 [Visit Diagnostics Assistant]({app_url})", unsafe_allow_html=True)

# ====================================
# 🖼️ MEDICAL IMAGING MODE
# ====================================
else:
    st.subheader("🖼️ Upload Medical Image for Diagnosis")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "dcm"])

    if uploaded_file:
        if uploaded_file.name.endswith(".dcm"):
            img = utils_preprocess.load_dicom(uploaded_file)
            result = ct_mri_model.CTMRIModel().predict(img)
            st.write("📊 CT/MRI Diagnosis:", result.tolist())
        else:
            img = utils_preprocess.load_and_preprocess(uploaded_file, target_size=(224, 224))
            
            model_choice = st.selectbox("Select Imaging Model", ["X-Ray", "Ultrasound"])
            if model_choice == "X-Ray":
                result = xray_model.XRayModel().predict(uploaded_file)
                st.write("📊 X-Ray Diagnosis:", result.tolist())
            elif model_choice == "Ultrasound":
                result = ultrasound_model.UltrasoundModel().predict(uploaded_file)
                st.write("📊 Ultrasound Diagnosis:", result.tolist())
# ====================================
# 🚀 SĀVI INTELLIGENCE FOOTER
# ====================================

# Helper function to load local image as Base64 (so it works on the web)
def get_base64_image(image_path):
    import base64
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 1. Get the logo path (ensure logo2.png is in your /static folder)
footer_logo_path = os.path.join(os.path.dirname(__file__), "static", "logo2.png")
logo_base64 = get_base64_image(footer_logo_path)

# 2. Define the HTML Structure
footer_html = f"""
<div style="margin-top: 150px;"></div> <footer style="
    background-color: #000; 
    padding: 60px 20px; 
    text-align: center; 
    border-top: 1px solid rgba(255,255,255,0.1); 
    margin-left: -100%; 
    margin-right: -100%;
">
    <div style="max-width: 800px; margin: 0 auto;">
        <img src="data:image/png;base64,{logo_base64}" alt="Sāvi Official Seal" style="width: 80px; height: auto; margin-bottom: 20px; opacity: 0.8;">
        <p style="color: #fff; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; font-size: 0.9rem; margin: 10px 0; font-family: 'Segoe UI', sans-serif;">
            SĀVI INTELLIGENCE
        </p>
        <div style="height: 2px; background: #f2a154; width: 40px; margin: 15px auto;"></div>
        <p style="color: #666; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; font-family: 'Segoe UI', sans-serif;">
            © 2026 All Rights Reserved | Seconds Matter
        </p>
    </div>
</footer>
"""

# 3. Inject into Streamlit
st.markdown(footer_html, unsafe_allow_html=True)

