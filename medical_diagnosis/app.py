import os
import streamlit as st
import base64
from ocr_utils import extract_text
from parser import extract_values
from modules.rule_based_engine import interpret_results
from modules.pdf_exporter import export_to_pdf

# ✅ Local CSS
def local_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("static/style.css")

# ✅ Text-to-Speech
def speak_text(text):
    escaped = text.replace('"', r'\"').replace('\n', ' ')
    st.markdown(f'''
        <script>
        var msg = new SpeechSynthesisUtterance("{escaped}");
        window.speechSynthesis.speak(msg);
        </script>
    ''', unsafe_allow_html=True)

# ✅ Page Config
st.set_page_config(page_title="Diagnostics Assistant", layout="centered")

st.title("👨‍⚕️ AI Medical Assistant")
st.markdown(
    '<div class="bot-avatar">'
    '<img src="https://media.giphy.com/media/UHAYP0FxJOmFBuOiC2/giphy.gif">'
    '</div>',
    unsafe_allow_html=True
)

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

        speak_text(summary.split("=== Recommendations ===")[0])

        # ✅ Generate PDF, upload, QR
        pdf_buffer, fileio_url, qr_path = export_to_pdf(name, age, gender, all_reports, summary)

        # ✅ Download (in-memory)
        st.markdown("### 📥 Download Report")
        st.download_button(
            label="📄 Download PDF Report (Direct)",
            data=pdf_buffer,
            file_name="report.pdf",
            mime="application/pdf"
        )

        # ✅ One-time link
        if fileio_url:
            st.markdown(f"🔗 [Click for One-Time Link]({fileio_url})", unsafe_allow_html=True)
        else:
            st.error("❌ Failed to generate one-time link.")

        # ✅ Show QR
        if os.path.exists(qr_path):
            st.image(qr_path, caption="📲 Scan to Download (One-Time Link)")
        else:
            st.info("QR not found.")
