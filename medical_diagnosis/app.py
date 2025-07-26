import streamlit as st
import os
from fpdf import FPDF
from PIL import Image

# Set page config
st.set_page_config(page_title="MEDONOSIS - Diagnosis Report", layout="centered")

# Load logo
logo_path = os.path.join("static", "MEDONOSIS.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=200)
else:
    st.error("Logo image not found at 'static/MEDONOSIS.png'")

st.markdown("### **MEDONOSIS**")
st.markdown("#### *Decode • Diagnose • Deliver*")
st.markdown("---")

# Input details
name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0, max_value=120)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
summary = st.text_area("Doctor Summary / Conclusion")

# Upload multiple medical reports
uploaded_reports = st.file_uploader("Upload medical report images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

def export_to_pdf(name, age, gender, reports, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="MEDONOSIS - Diagnosis Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Uploaded Reports:", ln=True)
    pdf.set_font("Arial", size=12)

    for img_file in reports:
        image = Image.open(img_file)
        temp_img_path = f"temp_{img_file.name}"
        image.save(temp_img_path)
        pdf.image(temp_img_path, w=180)
        os.remove(temp_img_path)
        pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Doctor's Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=summary)

    # QR Code
    qr_path = os.path.join("static", "qr.png")
    if os.path.exists(qr_path):
        pdf.image(qr_path, x=160, y=250, w=30)
    
    output_path = f"{name}_report.pdf"
    pdf.output(output_path)
    return output_path

# Button to generate PDF
if st.button("Generate PDF Report"):
    if not name or not summary or not uploaded_reports:
        st.warning("Please fill all fields and upload at least one report.")
    else:
        pdf_file_path = export_to_pdf(name, age, gender, uploaded_reports, summary)
        with open(pdf_file_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=os.path.basename(pdf_file_path))
        os.remove(pdf_file_path)
