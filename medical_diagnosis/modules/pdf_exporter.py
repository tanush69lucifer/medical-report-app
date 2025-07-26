from fpdf import FPDF
import qrcode
import io
import re
import os
import uuid
import requests
import streamlit as st
import json

def export_to_pdf(name, age, gender, reports, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False, margin=15)
    pdf.set_line_width(0.5)
    pdf.rect(10, 10, 190, 277)
    pdf.set_font("Helvetica", size=12)

    def clean(text):
        text = str(text)
        replacements = {"⚠": "[!]", "✓": "[OK]", "♥": "<3"}
        for symbol, replacement in replacements.items():
            text = text.replace(symbol, replacement)
        return re.sub(r'[^\x00-\x7F]', '', text)

    def safe_add_line(text, border=1, ln=True, fill=False):
        if pdf.get_y() > 270:
            pdf.add_page()
            pdf.rect(10, 10, 190, 277)
            pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 10, text, ln=ln, border=border, fill=fill)

    def safe_add_multicell(text, border=1):
        if pdf.get_y() > 260:
            pdf.add_page()
            pdf.rect(10, 10, 190, 277)
            pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(190, 10, txt=clean(text), border=border)

    # Header
    pdf.cell(0, 10, "Medical Diagnosis Report", ln=True, align="C", border=1)
    pdf.cell(0, 10, clean(f"Name: {name} | Age: {age} | Gender: {gender}"), ln=True, border=1)

    # Reports
    for idx, report in enumerate(reports):
        pdf.ln(5)
        safe_add_line(f"--- Report {idx+1} ---", fill=True)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.cell(60, 10, "Parameter", border=1)
        pdf.cell(60, 10, "Value", border=1)
        pdf.cell(60, 10, "Status", border=1)
        pdf.ln()
        pdf.set_font("Helvetica", size=11)
        for param, val in report.items():
            pdf.cell(60, 10, clean(param), border=1)
            pdf.cell(60, 10, clean(str(val['value'])), border=1)
            pdf.cell(60, 10, clean(val['status']), border=1)
            pdf.ln()

    # Summary
    pdf.ln(5)
    pdf.set_font("Helvetica", style="B", size=12)
    safe_add_line("--- Diagnosis Summary ---")
    pdf.set_font("Helvetica", size=11)
    for line in summary.split('\n'):
        safe_add_multicell(line)

    # Save PDF locally
    os.makedirs("export", exist_ok=True)
    local_path = f"export/report_{uuid.uuid4().hex[:8]}.pdf"
    pdf.output(local_path)

    # Upload to file.io safely
    fileio_url = None
    try:
        with open(local_path, "rb") as f:
            response = requests.post("https://file.io", files={"file": f})
            content_type = response.headers.get("Content-Type", "")

            if response.status_code == 200 and "application/json" in content_type:
                response_json = response.json()
                fileio_url = response_json.get("link")
            else:
                st.warning(f"⚠️ file.io upload returned unexpected content:\n{response.text}")
    except Exception as e:
        st.error("❌ Failed to upload to file.io")
        st.exception(e)

    # Generate QR
    qr_path = "export/qr.png"
    if fileio_url:
        try:
            qr_img = qrcode.make(fileio_url)
            qr_img.save(qr_path)

            # Add QR to PDF
            if pdf.get_y() > 230:
                pdf.add_page()
                pdf.rect(10, 10, 190, 277)

            pdf.ln(10)
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(0, 10, "Scan to Download", ln=True)
            pdf.image(qr_path, x=pdf.w - 60, y=pdf.get_y(), w=40)
        except Exception as e:
            st.warning("QR generation failed.")
            st.exception(e)

    # Return in-memory buffer for Streamlit
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    return pdf_buffer, fileio_url, qr_path
