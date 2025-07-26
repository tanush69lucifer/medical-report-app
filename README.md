# medical-report-app
An easy-to-use AI tool that reads your medical reports, explains key health markers, points out anything unusual, and gives you a clear summary with helpful suggestions. Quick, reliable, and comes with a QR code so you can access or share your report anytime, anywhere


- License

This project is licensed under the Apache License 2.0.



Project Summary
This prototype is a lightweight medical diagnosis report system. It allows users to input basic patient details and select or upload medical reports (like Creatinine or Liver Function Test results). Based on those inputs, it provides a diagnosis summary and treatment suggestions, and then exports a clean, printable PDF report.

What We’ve Built?
A simple web interface using Streamlit where users can:

Enter patient details (name, age, gender)
Select conditions (like diabetes, hypertension, etc.)
Upload or input test results
A rule-based engine that checks the test values against known medical thresholds to identify issues
A system that picks the right treatments/medications from a JSON-based medicine database
A PDF exporter that creates a neat report with diagnosis, suggested medicines, and health recommendations

Tools & Technologies Used
Python – core logic and backend
Streamlit – for the frontend UI
FPDF – for generating the final PDF report
PIL (Pillow) – for image handling if report screenshots are used
easyocr – to extract text from uploaded report images 
JSON – to store and retrieve medication data easily


How did we deploy ?
This app can run locally or be deployed on platforms like Streamlit Cloud by simply pushing the code to GitHub and connecting the repo. No heavy setup or login system is required , easy yet convinient. 


How It Works ?
User inputs patient details and specifies any condition if any for medicine as per age or problem constraint 
Selects or uploads a report (e.g., LFT or Creatinine)

The system simply:
Parses the report values
Matches values against predefined rules
Pulls relevant medications or advice from the medicine_db.json file
A PDF report is generated with all findings and treatment suggestions



